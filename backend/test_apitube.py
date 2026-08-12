import asyncio
from app.adapters.news.apitube_provider import APITubeProvider

async def main():
    provider = APITubeProvider()
    articles = await provider.search(query="", limit=10)  # fetches last 24h, AI topic
    print(f"Fetched {len(articles)} articles")
    for a in articles[:5]:  # show first 5
        print(f"- {a.title} ({a.source_name})")

if __name__ == "__main__":
    asyncio.run(main())