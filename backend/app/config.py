from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # FastAPI
    APP_NAME: str = "AI Daily News"
    DEBUG: bool = False

    # Supabase
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""

    # LLM (will add later)
    LLM_API_KEY: str = ""
    LLM_PROVIDER: str = "openai"

    # News
    APITUBE_API_KEY: str = ""
    NEWSDATA_API_KEY: str = ""
    ENABLED_NEWS_PROVIDERS: List[str] = ["apitube", "newsdata"]
    NEWS_QUERY: str = "AI OR artificial intelligence OR machine learning OR OpenAI OR Anthropic"
    APITUBE_TOPIC_ID: str = "industry.ai_news"
    NEWS_DATE_RANGE: int = 2

    NEWS_LIMIT_PER_PROVIDER: int = 50

    # Telegram
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()