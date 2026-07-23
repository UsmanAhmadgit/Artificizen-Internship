from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GROQ_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

try:
    settings = Settings()
except ValueError as e:
    raise RuntimeError("CRITICAL: GROQ_API_KEY is missing from the .env file. Hardcoding is prohibited.") from e

if not settings.GROQ_API_KEY.startswith("gsk_"):
    raise ValueError("CRITICAL: Invalid GROQ_API_KEY format detected. Ensure your real key is in the .env file.")