import asyncio
import logging
from app.services.image_generation_service import ImageGenerationService

logger = logging.getLogger(__name__)
REQUEST_DELAY = 3.0

async def generate_images_node(state: dict) -> dict:
    pending = state.get("pending_stories", [])   # <-- reads pending, not validated
    if not pending:
        return state

    service = ImageGenerationService()
    for idx, story in enumerate(pending):
        prompt = story.get("image_prompt")
        if not prompt:
            logger.warning(f"No prompt for story '{story.get('title', '')[:40]}...' – skipping")
            continue

        if idx > 0:
            await asyncio.sleep(REQUEST_DELAY)

        story_id = story.get("id", f"story_{idx}")
        file_path = await service.generate_and_save_local(prompt, story_id)
        if file_path:
            story["image_path"] = file_path
            logger.info(f"Image saved: {file_path}")
        else:
            story["image_path"] = None
            logger.error(f"Image generation failed for '{story.get('title', '')[:40]}...'")

    return state