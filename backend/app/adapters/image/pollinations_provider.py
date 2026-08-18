import httpx
import urllib.parse
import asyncio
import logging
from typing import Optional
from app.ports.iimage_generation_provider import IImageGenerationProvider

logger = logging.getLogger(__name__)

class PollinationsProvider(IImageGenerationProvider):
    async def generate_image(self, prompt: str) -> Optional[bytes]:
        encoded_prompt = urllib.parse.quote(prompt)
        # Try different models; 'flux' is default, 'flux-realism' is also good
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&model=flux"

        for attempt in range(3):
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.get(url)
                    if response.status_code == 200:
                        logger.info(f"Pollinations success (attempt {attempt+1})")
                        return response.content
                    elif response.status_code == 429:
                        wait = 2 ** attempt + 2  # 3s, 5s, 8s
                        logger.warning(f"Pollinations rate limited (attempt {attempt+1}). Waiting {wait}s...")
                        await asyncio.sleep(wait)
                        continue
                    else:
                        logger.error(f"Pollinations returned {response.status_code}")
                        return None
            except Exception as e:
                logger.error(f"Pollinations attempt {attempt+1} failed: {e}")
                if attempt < 2:
                    await asyncio.sleep(2 ** attempt)
                else:
                    return None
        return None