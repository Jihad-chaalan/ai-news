from abc import ABC, abstractmethod

class IPublisher(ABC):
    @abstractmethod
    async def publish(self, briefing_data: dict) -> bool:
        """Publish the briefing (e.g., to Telegram, email, etc.)."""
        pass