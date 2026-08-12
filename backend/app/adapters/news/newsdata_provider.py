import httpx
from datetime import datetime, timedelta
from typing import List
from app.models.article import Article
from app.ports.inews_provider import INewsProvider
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class NewsDataProvider(INewsProvider):
    BASE_URL = "https://newsdata.io/api/1/news"

    async def search(
        self,
        query: str,
        date_range: int = 2,
        limit: int = 40
    ) -> List[Article]:
        from_date = (datetime.utcnow() - timedelta(days=date_range)).strftime("%Y-%m-%d")

        params = {
            "apikey": settings.NEWSDATA_API_KEY,
            "q": query,
            "language": "en",
            "fromdatetime": from_date,
            "size": min(limit, 50),
            "sort": "relevance",
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

        articles = []
        for item in data.get("results", []):
            description = item.get("description") or item.get("title", "")
            article = Article(
                id=Article.generate_id(item.get("title", ""), item.get("link", "")),
                title=item.get("title", ""),
                description=description,
                api_summary=None,
                url=item.get("link", ""),
                published_at=datetime.fromisoformat(item.get("pubDate", "").replace("Z", "+00:00")),
                source_name=item.get("source_id", "Unknown"),
                provider="newsdata",
            )
            articles.append(article)

        logger.info(f"NewsData fetched {len(articles)} articles")
        return articles