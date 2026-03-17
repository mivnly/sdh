from pydantic import BaseModel, ConfigDict, PostgresDsn, SecretStr, computed_field
from pydantic.networks import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

from common.utils import setup_logger

# === Logger ===
log = setup_logger("app", "app.log")


# === DB ===
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)

    PG_DB: str
    PG_NAME: str
    PG_PORT: int
    PG_USER: str
    PG_PASS: SecretStr

    @computed_field
    @property
    def conn_url(self) -> PostgresDsn:
        obj = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            host=self.PG_DB,
            path=self.PG_NAME,
            port=self.PG_PORT,
            username=self.PG_USER,
            password=self.PG_PASS.get_secret_value(),
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
