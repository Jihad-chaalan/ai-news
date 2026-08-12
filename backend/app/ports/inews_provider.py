# abstract search(query, date_range, limit)
from abc import ABC, abstractmethod
from typing import List
from app.models.article import Article


class INewsProvider(ABC):
    """Contract for all news API adapters."""

    @abstractmethod
    async def search(
        self,
        query: str,
        date_range: int,      # days to look back
        limit: int
    ) -> List[Article]:
        """
        Fetch articles matching the query from the last `date_range` days.
        Returns a list of normalized Article objects.
        """
        pass