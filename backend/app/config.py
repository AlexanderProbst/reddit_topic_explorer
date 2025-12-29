from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    reddit_client_id: str | None = None
    reddit_client_secret: str | None = None
    reddit_user_agent: str = "reddit-analytics-app/0.1"
    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/reddit"
    hf_token: str | None = None
    anthropic_api_key: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()