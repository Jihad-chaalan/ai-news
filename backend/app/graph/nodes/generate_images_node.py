import asyncio
import logging
from app.services.image_generation_service import ImageGenerationService
from app.services.supabase_storage_service import SupabaseStorageService

logger = logging.getLogger(__name__)
REQUEST_DELAY = 3.0   # seconds between requests to avoid rate limits

async def generate_images_node(state: dict) -> dict:
    pending = state.get("pending_stories", [])
    if not pending:
        return state

    image_service = ImageGenerationService()
    storage_service = SupabaseStorageService()

    for idx, story in enumerate(pending):
        # Add delay between requests to avoid rate limits (Pollinations, etc.)
        if idx > 0:
            await asyncio.sleep(REQUEST_DELAY)

        prompt = story.get("image_prompt")
        if not prompt:
            logger.warning(f"No prompt for story '{story.get('title', '')[:40]}...' – skipping")
            continue

        story_id = story.get("id", f"story_{idx}")

        # 1. Generate image bytes (no local file)
        image_bytes = await image_service.generate_image(prompt)
        if not image_bytes:
            story["image_url"] = None
            logger.error(f"Image generation failed for '{story.get('title', '')[:40]}...'")
            continue

        # 2. Upload directly to Supabase
        public_url = await storage_service.upload_image_bytes(image_bytes, story_id)
        if public_url:
            story["image_url"] = public_url
            logger.info(f"Image uploaded: {public_url}")
        else:
            story["image_url"] = None
            logger.error(f"Supabase upload failed for '{story.get('title', '')[:40]}...'")

    return state