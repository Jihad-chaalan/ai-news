from pydantic import BaseModel, Field

class ImagePrompt(BaseModel):
    prompt: str = Field(..., description="Detailed editorial-style image prompt for AI image generation")