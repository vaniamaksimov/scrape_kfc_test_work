from dataclasses import dataclass
from enum import StrEnum
from typing import Annotated, Any, Callable, TypeAlias, TypeVar

from pydantic import BaseModel, UrlConstraints
from pydantic_core import MultiHostUrl, ValidationError
from pydantic_core import core_schema as cs

from src.core.database import Base

SqliteURL = Annotated[
    MultiHostUrl,
    UrlConstraints(
        allowed_schemes=[
            'sqlite+aiosqlite',
            'sqlite+pysqlite',
        ]
    ),
]


ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)
longitude: TypeAlias = float
latitude: TypeAlias = float


class OpenStatus(StrEnum):
    OPEN = 'Open'
    CLOSED = 'Closed'


class TimeZone(StrEnum):
    KALININGRAD = 'Europe/Kaliningrad'
    MOSCOW = 'Europe/Moscow'
    KIROV = 'Europe/Kirov'
    SAMARA = 'Europe/Samara'
    ULYANOVSK = 'Europe/Ulyanovsk'
    SARATOV = 'Europe/Saratov'
    ASTRAKHAN = 'Europe/Astrakhan'
    YEKATERINBURG = 'Asia/Yekaterinburg'
    OMSK = 'Asia/Omsk'
    KRASNOYARSK = 'Asia/Krasnoyarsk'
    NOVOSIBIRSK = 'Asia/Novosibirsk'
    TOMSK = 'Asia/Tomsk'
    NOVOKUZNETSK = 'Asia/Novokuznetsk'
    BARNAUL = 'Asia/Barnaul'
    IRKUTSK = 'Asia/Irkutsk'
    YAKUTSK = 'Asia/Yakutsk'
    CHITA = 'Asia/Chita'
    VLADIVOSTOK = 'Asia/Vladivostok'


_ERROR = object()


@dataclass
class ErorrItemsMarker:
    def __get_pydantic_core_schema__(
        self, source_type: Any, handler: Callable[[Any], cs.CoreSchema]
    ) -> cs.CoreSchema:
        schema = handler(source_type)

        def val(v: Any, handler: cs.ValidatorFunctionWrapHandler) -> Any:
            try:
                return handler(v)
            except ValidationError:
                return _ERROR

        return cs.no_info_wrap_validator_function(
            val, schema, serialization=schema.get('serialization')
        )


@dataclass
class ListErrorFilter:
    def __get_pydantic_core_schema__(
        self, source_type: Any, handler: Callable[[Any], cs.CoreSchema]
    ) -> cs.CoreSchema:
        schema = handler(source_type)

        def val(v: list[Any]) -> list[Any]:
            return [item for item in v if item is not _ERROR]

        return cs.no_info_after_validator_function(
            val, schema, serialization=schema.get('serialization')
        )


T = TypeVar('T')

LenientList = Annotated[list[Annotated[T, ErorrItemsMarker()]], ListErrorFilter()]


@dataclass
class ModeToFunction:
    @classmethod
    def parse(cls):
        from src.core.parse import parse

        return parse

    @classmethod
    def request(cls):
        from src.core.request import request

        return request
