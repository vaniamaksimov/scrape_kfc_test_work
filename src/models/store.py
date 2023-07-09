from datetime import time
from typing import TYPE_CHECKING

from sqlalchemy import Enum, Float, ForeignKey, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.base import Base
from src.core.settings import settings
from src.utils.app_types import OpenStatus, TimeZone

if TYPE_CHECKING:
    from src.models.city import City
    from src.models.feature import StoreFeature


class Store(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(
        String(settings.app.max_string_length), unique=True
    )
    address: Mapped[str] = mapped_column(String(settings.app.max_string_length))

    city_id: Mapped[str] = mapped_column(
        ForeignKey('city.id', name='fk_store_city'), nullable=False
    )
    city: Mapped['City'] = relationship(back_populates='stores')

    longitude: Mapped[float] = mapped_column(Float)
    latitude: Mapped[float] = mapped_column(Float)

    start_time_local: Mapped[time] = mapped_column(Time)
    end_time_local: Mapped[time] = mapped_column(Time)

    time_zone: Mapped[TimeZone] = mapped_column(Enum(TimeZone))
    status: Mapped[OpenStatus] = mapped_column(Enum(OpenStatus))

    store_features: Mapped[list['StoreFeature']] = relationship(back_populates='store')

    def __init__(
        self,
        id: int,
        name: str,
        address: str,
        city_id: str,
        longitude: float,
        latitude: float,
        start_time_local: time,
        end_time_local: time,
        time_zone: TimeZone,
        status: OpenStatus,
        store_features: list['StoreFeature'] = None,
    ):
        self.id = id
        self.name = name
        self.address = address
        self.city_id = city_id
        self.longitude = longitude
        self.latitude = latitude
        self.start_time_local = start_time_local
        self.end_time_local = end_time_local
        self.time_zone = time_zone
        self.status = status
        self.store_features = store_features or []
