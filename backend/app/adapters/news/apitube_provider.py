import httpx
from datetime import datetime, timedelta, timezone
from typing import List
from app.models.article import Article
from app.ports.inews_provider import INewsProvider
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class APITubeProvider(INewsProvider):
    BASE_URL = "https://api.apitube.io/v1/news/everything"

    async def search(
        self,
        query: str = "",
        date_range: int = 2,
        limit: int = 50
    ) -> List[Article]:
        now = datetime.now(timezone.utc)
        start_dt = now - timedelta(hours=24)

        start_str = start_dt.strftime("%Y-%m-%d")
        end_str = now.strftime("%Y-%m-%d")

        params_base = {
            "topic.id": settings.APITUBE_TOPIC_ID,
            "language.code": "en", 
            "published_at.start": start_str,
            "published_at.end": end_str,
            "sort.by": "published_at",
            "sort.order": "desc",
            "language": "en",
        }

        if query:
            params_base["q"] = query

        headers = {"X-API-Key": settings.APITUBE_API_KEY}

        all_articles = []
        page = 1
        fetched = 0

        async with httpx.AsyncClient(timeout=30.0) as client:
            while fetched < limit:
                params = params_base.copy()
                params["per_page"] = min(10, limit - fetched)
                params["page"] = page

                response = await client.get(self.BASE_URL, params=params, headers=headers)
                response.raise_for_status()
                data = response.json()

                results = data.get("results", [])
                if not results:
                    break

                for item in results:
                    # Use 'href' as the URL field (APITube's actual field name)
                    url = item.get("href") or item.get("url", "")
                    if not url:
                        # Skip articles without a URL
                        continue

                    description = item.get("description") or item.get("title", "")
                    pub_str = item.get("published_at", "")
                    if pub_str.endswith("Z"):
                        pub_str = pub_str.replace("Z", "+00:00")
                    published_at = datetime.fromisoformat(pub_str)
                    source = item.get("source", {})
                    source_name = source.get("domain") or source.get("id") or "Unknown"
                    article = Article(
                        id=Article.generate_id(item.get("title", ""), url),
                        title=item.get("title", ""),
                        description=description,
                        api_summary=None,
                        url=url,
                        published_at=published_at,
                        source_name=source_name,
                        provider="apitube",
                    )
                    all_articles.append(article)
                    fetched += 1

                if not data.get("has_next_pages", False):
                    break
                page += 1

        logger.info(f"APITube fetched {len(all_articles)} articles")
        return all_articles