from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # FastAPI
    APP_NAME: str = "AI Daily News"
    DEBUG: bool = False

    # Supabase
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""

    # LLM 
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "openai/gpt-oss-120b" 

    # News
    APITUBE_API_KEY: str = ""
    NEWSDATA_API_KEY: str = ""
    ENABLED_NEWS_PROVIDERS: List[str] = ["apitube", "newsdata"]
    NEWS_QUERY: str = "artificial intelligence"
    APITUBE_TOPIC_ID: str = "industry.ai_news"
    NEWS_DATE_RANGE: int = 2

    NEWS_LIMIT_PER_PROVIDER: int = 20

    # Telegram
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()