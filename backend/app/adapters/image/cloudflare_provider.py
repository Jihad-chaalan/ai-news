import httpx
import base64
import logging
from typing import Optional
from app.config import settings
from app.ports.iimage_generation_provider import IImageGenerationProvider

logger = logging.getLogger(__name__)

class CloudflareImageProvider(IImageGenerationProvider):
    def __init__(self):
        self.api_token = settings.CLOUDFLARE_API_TOKEN
        self.account_id = settings.CLOUDFLARE_ACCOUNT_ID
        self.model = settings.CLOUDFLARE_MODEL
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/{self.model}"

    async def generate_image(self, prompt: str) -> Optional[bytes]:
        if not self.api_token or not self.account_id:
            logger.warning("Cloudflare credentials missing – skipping provider")
            return None
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        payload = {"prompt": prompt}

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(self.base_url, json=payload, headers=headers)
                if response.status_code == 200:
                    # Check if binary or JSON
                    content_type = response.headers.get('content-type', '')
                    if 'image' in content_type:
                        return response.content
                    else:
                        data = response.json()
                        if data.get("success"):
                            image_b64 = data.get("result", {}).get("image")
                            if image_b64:
                                return base64.b64decode(image_b64)
                else:
                    logger.error(f"Cloudflare returned status {response.status_code}")
                return None
            except Exception as e:
                logger.error(f"Cloudflare generation failed: {e}")
                return None