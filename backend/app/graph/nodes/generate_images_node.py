import asyncio
import logging
import uuid
from app.services.image_generation_service import ImageGenerationService
from app.services.supabase_storage_service import SupabaseStorageService

logger = logging.getLogger(__name__)
REQUEST_DELAY = 3.0

async def generate_images_node(state: dict) -> dict:
    pending = state.get("pending_stories", [])
    if not pending:
        return state

    image_service = ImageGenerationService()
    storage_service = SupabaseStorageService()

    for idx, story in enumerate(pending):
        if idx > 0:
            await asyncio.sleep(REQUEST_DELAY)

        prompt = story.get("image_prompt")
        if not prompt:
            logger.warning(f"No prompt for story '{story.get('title', '')[:40]}...' – skipping")
            continue

        # Generate a unique filename with timestamp + random suffix
        unique_id = f"{uuid.uuid4().hex[:8]}"
        story_id = story.get("id", f"story_{idx}")
        filename = f"{story_id}_{unique_id}"  # e.g., story_0_a1b2c3d4

        # Generate image bytes
        image_bytes = await image_service.generate_image(prompt)
        if not image_bytes:
            story["image_url"] = None
            logger.error(f"Image generation failed for '{story.get('title', '')[:40]}...'")
            continue

        # Upload to Supabase with unique filename
        public_url = await storage_service.upload_image_bytes(image_bytes, filename)
        if public_url:
            story["image_url"] = public_url
            logger.info(f"Image uploaded: {public_url}")
        else:
            story["image_url"] = None
            logger.error(f"Supabase upload failed for '{story.get('title', '')[:40]}...'")

    return state