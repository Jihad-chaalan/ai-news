import logging
from typing import List, Optional
from app.ports.iimage_generation_provider import IImageGenerationProvider
from app.adapters.image.cloudflare_provider import CloudflareImageProvider
from app.adapters.image.pollinations_provider import PollinationsProvider

logger = logging.getLogger(__name__)

class ImageGenerationService:
    def __init__(self):
        self.providers: List[IImageGenerationProvider] = [
            CloudflareImageProvider(),
            PollinationsProvider(),
            # Add more fallbacks here if needed
        ]

    async def generate_image(self, prompt: str) -> Optional[bytes]:
        """
        Try each provider in order and return image bytes if successful.
        """
        for idx, provider in enumerate(self.providers):
            try:
                logger.info(f"Trying image provider {idx+1}/{len(self.providers)}...")
                image_data = await provider.generate_image(prompt)
                if image_data:
                    logger.info(f"Image generated successfully by provider {idx+1}")
                    return image_data
                else:
                    logger.warning(f"Provider {idx+1} returned no data, trying next...")
            except Exception as e:
                logger.error(f"Provider {idx+1} failed: {e}")
                continue
        logger.error("All image providers failed")
        return None

    # Keep this if you still want local saving for debugging, but remove if not needed
    async def generate_and_save_local(self, prompt: str, story_id: str) -> Optional[str]:
        image_data = await self.generate_image(prompt)
        if not image_data:
            return None

        import os
        from datetime import datetime
        os.makedirs("generated_images", exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"generated_images/story_{story_id}_{timestamp}.png"
        with open(filename, "wb") as f:
            f.write(image_data)
        return filename