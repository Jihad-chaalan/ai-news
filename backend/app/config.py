from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # FastAPI
    APP_NAME: str = "AI Daily News"
    DEBUG: bool = False

    # Supabase
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    SUPABASE_BUCKET: str = "ai-news-images"

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

    #Image LLM
    CLOUDFLARE_ACCOUNT_ID: str = ""
    CLOUDFLARE_API_TOKEN: str = ""
    CLOUDFLARE_MODEL: str = "@cf/stabilityai/stable-diffusion-xl-base-1.0"


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()