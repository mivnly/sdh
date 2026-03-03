from pydantic import BaseModel, ConfigDict, PostgresDsn, SecretStr, computed_field
from pydantic.networks import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

from common.utils import setup_logger

# === Logger ===
log = setup_logger("app", "app.log")


# === DB ===
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="forbid", case_sensitive=True)

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


settings = Settings()  # type: ignore


# === URLS ===
class AppUrls(BaseModel):
    model_config = ConfigDict(extra="forbid")

    base_url: HttpUrl
    api_path: str

    @computed_field
    @property
    def api_url(self) -> HttpUrl:
        return HttpUrl(self.base_url.encoded_string() + self.api_path)


app_urls = AppUrls(base_url=HttpUrl("http://127.0.0.1:8000/"), api_path="api/v1")
