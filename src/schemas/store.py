from datetime import time

from pydantic import BaseModel, ConfigDict, Extra

from src.utils.app_types import OpenStatus, TimeZone


class StoreBase(BaseModel):
    model_config = ConfigDict(extra=Extra.forbid)


class StoreCreate(StoreBase):
    id: int
    name: str
    address: str
    city_id: str
    longitude: float
    latitude: float
    start_time_local: time
    end_time_local: time
    time_zone: TimeZone
    status: OpenStatus


class StoreUpdate(StoreBase):
    name: str | None
    address: str | None
    city_id: str | None
    longitude: float | None
    latitude: float | None
    start_time_local: time | None
    end_time_local: time | None
    time_zone: TimeZone | None
    status: OpenStatus | None


class StoreDB(BaseModel):
    id: int
    name: str
    adress: str
    city_id: str
    longitude: float
    latitude: float
    start_time_local: time
    end_time_local: time
    time_zone: TimeZone
    status: OpenStatus

    model_config = ConfigDict(from_attributes=True)
