import asyncio
import logging
from datetime import datetime, timezone
from typing import List, Optional

import httpx
from httpx import HTTPStatusError

from app.config import settings
from app.models.article import Article
from app.ports.inews_provider import INewsProvider

logger = logging.getLogger(__name__)


class NewsDataProvider(INewsProvider):
    BASE_URL = "https://newsdata.io/api/1/latest"

    # Refined AI keyword list – helps filter out non‑AI stories
    AI_KEYWORDS = [
        "AI", "artificial intelligence", "machine learning", "deep learning",
        "OpenAI", "Anthropic", "Google", "Gemini", "Claude", "LLM",
        "large language", "neural network", "generative", "AGI",
        "ChatGPT", "Copilot", "Llama", "Mistral", "Stable Diffusion",
        "NVIDIA", "GPU", "inference", "training", "model", "agent",
        "neural", "NLP", "natural language", "transformer", "BERT",
        "GPT", "Bard", "DeepMind"
    ]

    def _is_ai_related(self, title: str) -> bool:
        """Check if title contains AI‑related keywords."""
        title_lower = title.lower()
        return any(kw.lower() in title_lower for kw in self.AI_KEYWORDS)

    @staticmethod
    def _is_english(text: str) -> bool:
        """Heuristic: text is mostly ASCII (English)."""
        if not text:
            return False
        ascii_count = sum(1 for c in text if ord(c) < 128)
        return ascii_count / len(text) > 0.7

    async def _make_request(
        self, client: httpx.AsyncClient, params: dict, max_retries: int = 3
    ) -> dict:
        """Make a request with exponential backoff on 429 (rate limit)."""
        base_delay = 2  # seconds
        for attempt in range(max_retries):
            try:
                response = await client.get(self.BASE_URL, params=params)
                response.raise_for_status()
                return response.json()
            except HTTPStatusError as e:
                if e.response.status_code == 429:
                    # Retry‑After header may be present
                    retry_after = e.response.headers.get("Retry-After")
                    if retry_after and retry_after.isdigit():
                        wait = int(retry_after)
                    else:
                        wait = base_delay * (2 ** attempt)  # exponential backoff
                    logger.warning(
                        f"NewsData rate limit (429). Attempt {attempt+1}/{max_retries}. "
                        f"Waiting {wait}s..."
                    )
                    await asyncio.sleep(wait)
                    continue
                # Other HTTP errors – re-raise
                raise
        # If we've exhausted retries
        raise Exception(f"NewsData request failed after {max_retries} retries.")

    async def search(
        self,
        query: str = "",
        date_range: int = 2,   # not used for /latest, kept for interface
        limit: int = 40
    ) -> List[Article]:
        """
        Fetch articles from NewsData.io, using `/latest` endpoint.
        Filters by `q=artificial intelligence`, language=en, category=technology,
        and applies a strict title‑based AI keyword filter.
        """
        search_query = query or "artificial intelligence"

        # Base parameters – static for all pages
        params_base = {
            "apikey": settings.NEWSDATA_API_KEY,
            "q": search_query,
            "language": "en",
            "category": "technology",
            "removeduplicate": 1,
            "size": 10,                # max per page (free tier allows 10)
        }

        all_articles: List[Article] = []
        next_page: Optional[str] = None
        fetched = 0

        async with httpx.AsyncClient(timeout=30.0) as client:
            while fetched < limit:
                params = params_base.copy()
                if next_page:
                    params["page"] = next_page

                # Limit the size of this page so we don't exceed `limit`
                page_size = min(10, limit - fetched)
                params["size"] = page_size

                try:
                    data = await self._make_request(client, params)
                except Exception as e:
                    logger.error(f"NewsData request failed: {e}")
                    break   # stop pagination on error

                # Check API status
                if data.get("status") != "success":
                    logger.error(f"NewsData API error: {data.get('message', 'unknown error')}")
                    break

                results = data.get("results", [])
                if not results:
                    break

                for item in results:
                    title = item.get("title", "")
                    url = item.get("link", "")
                    if not title or not url:
                        continue

                    # --- Strict filters ---
                    if not self._is_english(title):
                        continue
                    if not self._is_ai_related(title):
                        continue
                    # -----------------------

                    description = item.get("description") or title

                    # Parse publication date (format: "2026-08-11 23:50:17")
                    pub_str = item.get("pubDate", "")
                    if pub_str:
                        try:
                            published_at = datetime.strptime(
                                pub_str, "%Y-%m-%d %H:%M:%S"
                            ).replace(tzinfo=timezone.utc)
                        except ValueError:
                            # fallback: try ISO format
                            pub_str = pub_str.replace("Z", "+00:00")
                            published_at = datetime.fromisoformat(pub_str)
                    else:
                        published_at = datetime.now(timezone.utc)

                    article = Article(
                        id=Article.generate_id(title, url),
                        title=title,
                        description=description,
                        api_summary=None,
                        url=url,
                        published_at=published_at,
                        source_name=item.get("source_name") or item.get("source_id", "Unknown"),
                        provider="newsdata",
                    )
                    all_articles.append(article)
                    fetched += 1

                # Check for next page token
                next_page = data.get("nextPage")
                if not next_page:
                    break

        logger.info(f"NewsData fetched {len(all_articles)} articles")
        return all_articles