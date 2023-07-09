import argparse
from abc import ABC
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.utils.app_types import ModeToFunction, SqliteURL
from src.utils.dsn import SqliteDsn


class ABCSettings(BaseSettings, ABC):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', case_sensitive=False, extra='ignore'
    )


class AppSettings(ABCSettings):
    max_string_length: int = 255


class DbSettings(ABCSettings):
    scheme: str = Field(..., validation_alias='SQLITE_SCHEME')
    db_path: str = Field(..., validation_alias='SQLITE_PATH')
    url: SqliteURL | None = None

    @validator('url')
    def url_validator(cls, value: str | None, values: dict[str, str]) -> str:
        if isinstance(value, str):
            return value
        return SqliteDsn.build(scheme=values.get('scheme'), path=values.get('db_path'))


class Settings(BaseModel):
    app: AppSettings = AppSettings()
    db: DbSettings = DbSettings()
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description='Парсер KFC')

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def model_post_init(self, __context: Any) -> None:
        self.parser.add_argument(
            'usage',
            choices=[
                choice
                for choice in ModeToFunction.__dict__.keys()
                if not choice.startswith('_')
            ],
            help='Режим работы',
        )


settings = Settings()
