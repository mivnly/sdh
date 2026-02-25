import logging

from pydantic import PostgresDsn, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

# === Logger ===

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(filename)s::%(funcName)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

log = logging.getLogger("app")


# === DB ===

class Settings(BaseSettings):

    DB_HOST: str
    DB_NAME: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: SecretStr

    @computed_field
    @property
    def conn_url(self) -> PostgresDsn:
        obj = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            host=self.DB_HOST,
            path=self.DB_NAME,
            port=self.DB_PORT,
            username=self.DB_USER,
            password=self.DB_PASS.get_secret_value(),
        )
        return obj

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra="forbid",
        case_sensitive=True
    )

settings = Settings() #type: ignore
