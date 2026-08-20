import logging
from supabase import create_client, Client
from app.config import settings

logger = logging.getLogger(__name__)

class SupabaseStorageService:
    def __init__(self):
        self.url = settings.SUPABASE_URL
        self.key = settings.SUPABASE_KEY
        self.bucket = settings.SUPABASE_BUCKET
        self.client: Client = create_client(self.url, self.key)

    async def upload_image_bytes(self, image_bytes: bytes, story_id: str) -> str:
        """
        Upload image bytes directly to Supabase Storage and return public URL.
        """
        try:
            storage_path = f"stories/{story_id}.png"
            response = self.client.storage.from_(self.bucket).upload(
                path=storage_path,
                file=image_bytes,
                file_options={"content-type": "image/png"}
            )
            if response:
                public_url = self.client.storage.from_(self.bucket).get_public_url(storage_path)
                logger.info(f"Image uploaded: {public_url}")
                return public_url
            else:
                logger.error(f"Upload failed: {response}")
                return None
        except Exception as e:
            logger.error(f"Supabase upload failed: {e}")
            return None