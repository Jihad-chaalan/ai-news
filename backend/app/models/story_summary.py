from pydantic import BaseModel, Field
from typing import List

class StorySummary(BaseModel):
    title: str = Field(..., description="Concise, catchy headline")
    summary: str = Field(..., description="2-3 sentence summary of the story")
    why_it_matters: str = Field(..., description="1-2 sentence explanation of why this is important")
    key_points: List[str] = Field(..., description="3 bullet points (key takeaways)", min_items=2, max_items=4)