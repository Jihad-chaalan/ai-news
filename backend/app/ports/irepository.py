from abc import ABC, abstractmethod

class IRepository(ABC):
    @abstractmethod
    async def save_briefing(self, briefing_data: dict) -> bool:
        """Save a complete briefing (with stories and sources) to the database."""
        pass