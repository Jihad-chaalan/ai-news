# abstract generate(prompt, response_model)

from abc import ABC, abstractmethod
from typing import Type, TypeVar

T = TypeVar('T', bound='BaseModel')

class ILLMProvider(ABC):
    @abstractmethod
    async def generate_structured(
        self,
        prompt: str,
        response_model: Type[T],
        temperature: float = 0.3
    ) -> T:
        """Generate a structured output (JSON) from the LLM, parsed into the given Pydantic model."""
        pass