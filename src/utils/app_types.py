from dataclasses import dataclass
from enum import StrEnum
from typing import Annotated, Any, Callable, TypeAlias, TypeVar

from pydantic import BaseModel, UrlConstraints
from pydantic_core import MultiHostUrl, ValidationError
from pydantic_core import core_schema as cs

from src.core.database import Base
from src.core.parse import parse
from src.core.request import request

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


class TimeZone(StrEnum):
    KALININGRAD = 'Europe/Kaliningrad'  # +2
    MOSCOW = 'Europe/Moscow'  # +3
    KIROV = 'Europe/Kirov'  # +3
    SAMARA = 'Europe/Samara'  # +4
    ULYANOVSK = 'Europe/Ulyanovsk'  # +4
    SARATOV = 'Europe/Saratov'  # +4
    ASTRAKHAN = 'Europe/Astrakhan'  # + 4
    YEKATERINBURG = 'Asia/Yekaterinburg'  # +5
    OMSK = 'Asia/Omsk'  # +6
    KRASNOYARSK = 'Asia/Krasnoyarsk'  # +7
    NOVOSIBIRSK = 'Asia/Novosibirsk'  # +7
    TOMSK = 'Asia/Tomsk'  # +7
    NOVOKUZNETSK = 'Asia/Novokuznetsk'  # +7
    BARNAUL = 'Asia/Barnaul'  # +7
    IRKUTSK = 'Asia/Irkutsk'  # +8
    YAKUTSK = 'Asia/Yakutsk'  # +9
    CHITA = 'Asia/Chita'  # +9
    VLADIVOSTOK = 'Asia/Vladivostok'  # +10


class OpenStatus(StrEnum):
    OPEN = 'Open'
    CLOSE = 'Closed'


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
    parse: Callable[[], None] = parse
    request: Callable[[], None] = request
