from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "your_secret_key"
    ADMIN_PASSWORD: str = "your_admin_password"

settings = Settings()
