import json
import asyncio
from typing import Type, TypeVar
from pydantic import BaseModel
from groq import AsyncGroq
from app.config import settings
from app.ports.illm_provider import ILLMProvider
import logging

logger = logging.getLogger(__name__)
T = TypeVar('T', bound=BaseModel)

class GroqProvider(ILLMProvider):
    def __init__(self, model: str = None):
        self.model = model or settings.GROQ_MODEL
        self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)

    async def generate_structured(
        self,
        prompt: str,
        response_model: Type[T],
        temperature: float = 0.3,
        max_tokens: int = 512   # Reduced from 1024
    ) -> T:
        # Shorten system prompt
        schema = response_model.model_json_schema()
        schema_str = json.dumps(schema)

        system_prompt = f"""
You are an AI news editor. Score the story on 0-10 for:
- industry_impact
- technical_significance
- audience_interest
- novelty
- overall_importance
Return a JSON object exactly matching this schema:
{schema_str}
"""

        # Shorten user prompt: truncate description to 200 chars
        # The prompt already contains description; we can truncate before sending.
        # But we'll modify build_prompt in ranking_node to shorten description.

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                response_format={"type": "json_object"},
                max_tokens=max_tokens,
            )
            content = response.choices[0].message.content
            parsed = response_model.model_validate_json(content)
            return parsed
        except Exception as e:
            logger.error(f"Groq API error: {e}")
            raise