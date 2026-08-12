import asyncio
from app.adapters.news.newsdata_provider import NewsDataProvider

async def main():
    provider = NewsDataProvider()
    articles = await provider.search(limit=10)
    print(f"Fetched {len(articles)} articles")
    for a in articles[:5]:
        print(f"- {a.title} ({a.source_name})")

if __name__ == "__main__":
    asyncio.run(main())