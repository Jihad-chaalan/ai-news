import logging
import asyncio
from datetime import datetime, timedelta, timezone
from supabase import create_client, Client
import httpx
from app.config import settings

logger = logging.getLogger(__name__)

class CleanupService:
    def __init__(self):
        # Use default client – retry logic will handle transient errors
        self.client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        self.bucket = settings.SUPABASE_BUCKET

    async def _execute_with_retry(self, query_func, max_retries=3):
        """Execute a Supabase query with retries on connection errors."""
        for attempt in range(max_retries):
            try:
                return query_func()
            except (httpx.RemoteProtocolError, httpx.ReadTimeout, httpx.ConnectTimeout) as e:
                if attempt == max_retries - 1:
                    raise
                wait = 2 ** attempt
                logger.warning(f"Supabase connection error (attempt {attempt+1}/{max_retries}), retrying in {wait}s: {e}")
                await asyncio.sleep(wait)
            except Exception as e:
                # Non‑retryable errors – re-raise immediately
                raise

    async def delete_old_briefings(self, retention_days: int = 7) -> int:
        # 1. Calculate cutoff date
        cutoff = (datetime.now(timezone.utc) - timedelta(days=retention_days)).date().isoformat()
        logger.info(f"📅 Cutoff date: {cutoff}")

        # 2. Debug: fetch ALL briefings to see what exists
        all_briefings = self.client.table("briefings").select("id, date").execute()
        logger.info(f"📋 All briefings in DB: {all_briefings.data}")

        # 3. Get old briefings (date < cutoff)
        def get_briefings():
            return self.client.table("briefings")\
                .select("id, date")\
                .lt("date", cutoff)\
                .execute()

        briefing_res = await self._execute_with_retry(get_briefings)
        logger.info(f"🔍 Old briefings query returned {len(briefing_res.data)} rows: {briefing_res.data}")

        if not briefing_res.data:
            logger.info("No old briefings found.")
            return 0

        briefing_ids = [row["id"] for row in briefing_res.data]
        logger.info(f"🗑️ Briefing IDs to delete: {briefing_ids}")

        # 4. Get images for these briefings
        def get_images():
            return self.client.table("stories")\
                .select("image_url")\
                .in_("briefing_id", briefing_ids)\
                .execute()

        stories_res = await self._execute_with_retry(get_images)
        image_urls = [row["image_url"] for row in stories_res.data if row.get("image_url")]
        logger.info(f"🖼️ Found {len(image_urls)} images to delete.")

        # 5. Delete images from Storage
        for url in image_urls:
            try:
                if "/public/" in url:
                    path = url.split("/public/")[1]
                    if "?" in path:
                        path = path.split("?")[0]
                    # ---- FIX: Remove bucket name from path ----
                    if path.startswith(settings.SUPABASE_BUCKET + "/"):
                        path = path[len(settings.SUPABASE_BUCKET) + 1:]
                    # -------------------------------------------
                    logger.info(f"Deleting image: {path}")
                    self.client.storage.from_(self.bucket).remove([path])
                    logger.info(f"Successfully deleted image: {path}")
                else:
                    logger.warning(f"Could not extract path from URL: {url}")
            except Exception as e:
                logger.error(f"Failed to delete image {url}: {e}")

        # 6. Delete briefings (cascade)
        for bid in briefing_ids:
            try:
                self.client.table("briefings").delete().eq("id", bid).execute()
                logger.info(f"Deleted briefing {bid}")
            except Exception as e:
                logger.error(f"Failed to delete briefing {bid}: {e}")

        return len(briefing_ids)