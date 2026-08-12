import asyncio
import httpx
from app.config import settings

async def debug():
    url = "https://api.apitube.io/v1/news/everything"
    params = {
        "topic.id": "industry.ai_news",
        "published_at.start": "2026-08-11",
        "published_at.end": "2026-08-12",
        "per_page": 10,
        "language": "en",
        "sort.by": "published_at",
        "sort.order": "desc",
    }
    headers = {"X-API-Key": settings.APITUBE_API_KEY}

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(url, params=params, headers=headers)
        print("Status:", resp.status_code)
        print("Response JSON keys:", resp.json().keys())
        print("Full response (first 1000 chars):")
        print(resp.text[:1000])

if __name__ == "__main__":
    asyncio.run(debug())