from abc import ABC, abstractmethod
from typing import Optional

class IImageGenerationProvider(ABC):
    """
    Abstract interface for image generation providers.
    All image providers (Cloudflare, Pollinations, etc.) must implement this.
    """

    @abstractmethod
    async def generate_image(self, prompt: str) -> Optional[bytes]:
        """
        Generate an image from the given prompt.

        Args:
            prompt: The text prompt describing the image.

        Returns:
            Optional[bytes]: The image data as bytes, or None if generation failed.
        """
        pass