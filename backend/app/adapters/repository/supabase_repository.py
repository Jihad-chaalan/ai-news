import logging
from datetime import date, timedelta
from supabase import create_client, Client
from app.ports.irepository import IRepository
from app.config import settings

logger = logging.getLogger(__name__)

class SupabaseRepository(IRepository):
    def __init__(self):
        self.client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

    # ====================== WRITE ======================
    async def briefing_exists(self, date_str: str) -> bool:
        """Check if a briefing already exists for the given date."""
        try:
            res = self.client.table("briefings").select("id").eq("date", date_str).execute()
            return len(res.data) > 0
        except Exception as e:
            logger.error(f"Failed to check briefing existence: {e}")
            return False

    async def save_briefing(self, briefing_data: dict) -> bool:
        """
        Save a complete briefing (with stories and sources) to the database.
        Idempotent: skips if briefing for that date already exists.
        """
        date_str = briefing_data["date"].isoformat()
        if await self.briefing_exists(date_str):
            logger.info(f"Briefing for {date_str} already exists – skipping insert.")
            return True  # idempotent: treat as success

        try:
            # 1. Insert briefing
            briefing = {"date": date_str}
            briefing_res = self.client.table("briefings").insert(briefing).execute()
            briefing_id = briefing_res.data[0]["id"]

            # 2. Insert stories
            for idx, story_data in enumerate(briefing_data["stories"]):
                try:
                    # Ensure key_points is a list
                    key_points = story_data.get("key_points") or []

                    # Convert HttpUrl to string if present
                    image_url = story_data.get("image_url")
                    if image_url:
                        image_url = str(image_url)

                    story = {
                        "briefing_id": briefing_id,
                        "title": story_data["title"],
                        "summary": story_data["summary"],
                        "why_it_matters": story_data["why_it_matters"],
                        "key_points": key_points,
                        "image_url": image_url,
                        "importance_score": story_data.get("importance_score", 0),
                    }
                    story_res = self.client.table("stories").insert(story).execute()
                    story_id = story_res.data[0]["id"]

                    # 3. Insert sources for this story
                    for source in story_data.get("sources", []):
                        source_url = source.get("url")
                        if source_url:
                            source_url = str(source_url)

                        source_data = {
                            "story_id": story_id,
                            "url": source_url,
                            "publisher": source.get("publisher", "Unknown"),
                            "published_at": source.get("published_at"),
                        }
                        self.client.table("sources").insert(source_data).execute()

                    logger.info(f"Saved story {idx+1}/{len(briefing_data['stories'])}")
                except Exception as e:
                    logger.error(f"Failed to save story {idx+1}: {e}")
                    logger.error(f"Story data: {story_data}")
                    return False

            logger.info(f"Saved briefing for {briefing_data['date']}")
            return True
        except Exception as e:
            logger.error(f"Failed to save briefing: {e}")
            return False

    # ====================== READ ======================
    async def get_briefing_by_date(self, date_str: str) -> dict:
        """Fetch a complete briefing (stories + sources) for a given date (YYYY-MM-DD)."""
        try:
            briefing_res = self.client.table("briefings")\
                .select("*")\
                .eq("date", date_str)\
                .execute()
            if not briefing_res.data:
                return None
            briefing = briefing_res.data[0]

            stories_res = self.client.table("stories")\
                .select("*")\
                .eq("briefing_id", briefing["id"])\
                .order("importance_score", desc=True)\
                .execute()
            briefing["stories"] = stories_res.data

            for story in briefing["stories"]:
                sources_res = self.client.table("sources")\
                    .select("*")\
                    .eq("story_id", story["id"])\
                    .execute()
                story["sources"] = sources_res.data

            return briefing
        except Exception as e:
            logger.error(f"Failed to fetch briefing for {date_str}: {e}")
            return None

    async def get_briefing_dates(self) -> list:
        """Return list of the last 7 days' briefing dates (as strings)."""
        try:
            cutoff = (date.today() - timedelta(days=7)).isoformat()
            res = self.client.table("briefings")\
                .select("date")\
                .gte("date", cutoff)\
                .order("date", desc=True)\
                .execute()
            return [row["date"] for row in res.data]
        except Exception as e:
            logger.error(f"Failed to fetch briefing dates: {e}")
            return []

    # ====================== DELETE ======================
    async def delete_briefing(self, briefing_id: str) -> bool:
        """Delete a briefing and all related stories/sources (cascade)."""
        try:
            self.client.table("briefings").delete().eq("id", briefing_id).execute()
            logger.info(f"Deleted briefing {briefing_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete briefing {briefing_id}: {e}")
            return False