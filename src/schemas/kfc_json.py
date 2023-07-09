from datetime import time

from pydantic import UUID4, BaseModel, field_validator

from src.utils.app_types import LenientList, OpenStatus, TimeZone, latitude, longitude
from src.utils.validators import time_validator


class RegularJson(BaseModel):
    startTimeLocal: time
    endTimeLocal: time

    normalize_startTimeLocal = field_validator('startTimeLocal', mode='before')(
        time_validator
    )
    normalize_endTimeLocal = field_validator('endTimeLocal', mode='before')(
        time_validator
    )


class OpeningHoursJson(BaseModel):
    regular: RegularJson


class GeometryJson(BaseModel):
    coordinates: tuple[longitude, latitude]


class CoodrinatesJson(BaseModel):
    geometry: GeometryJson


class CityJson(BaseModel):
    ru: str


class AdressJson(BaseModel):
    ru: str


class ContactsJson(BaseModel):
    streetAddress: AdressJson
    city: CityJson
    coordinates: CoodrinatesJson


class TitleJson(BaseModel):
    ru: str


class StoreJson(BaseModel):
    storeId: int
    kfcCityId: UUID4
    title: TitleJson
    contacts: ContactsJson
    openingHours: OpeningHoursJson
    timeZone: TimeZone
    status: OpenStatus
    features: list[
        str
    ]  # TODO M2M 'driveIn', 'wifi', 'breakfast', 'walkupWindow', '24hours'


class ResultJson(BaseModel):
    storePublic: StoreJson


class KfcJson(BaseModel):
    searchResults: LenientList[ResultJson]
