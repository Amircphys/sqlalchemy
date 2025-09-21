import os
from dotenv import load_dotenv


load_dotenv()
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str|None
    DB_PORT: str|None
    DB_USER: str|None
    DB_PASS: str|None
    DB_NAME: str|None
    
    @property
    def database_url(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    


settings = Settings(
    DB_HOST=os.getenv('DB_HOST'),
    DB_PORT=os.getenv('DB_PORT'),
    DB_USER=os.getenv('DB_USER'),
    DB_PASS=os.getenv('DB_PASS'),
    DB_NAME=os.getenv('DB_NAME'),
)
