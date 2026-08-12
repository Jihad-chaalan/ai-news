# Article Pydantic model

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, HttpUrl, Field


class Article(BaseModel):
    """Normalized article from any news provider."""
    id: str = Field(..., description="Unique hash (title + url)")
    title: str
    description: str                    
    api_summary: Optional[str] = None    # Only from APITube
    url: HttpUrl
    published_at: datetime
    source_name: str
    provider: str                        # 'apitube' or 'newsdata'

    @classmethod
    def generate_id(cls, title: str, url: str) -> str:
        import hashlib
        return hashlib.md5(f"{title}{url}".encode()).hexdigest()