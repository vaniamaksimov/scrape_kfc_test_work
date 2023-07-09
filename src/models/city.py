from typing import TYPE_CHECKING

from sqlalchemy import String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.base import Base
from src.core.settings import settings

if TYPE_CHECKING:
    from src.models.store import Store


class City(Base):
    id: Mapped[str] = mapped_column(Uuid(as_uuid=False), primary_key=True)
    name: Mapped[str] = mapped_column(
        String(settings.app.max_string_length), unique=False
    )
    stores: Mapped[list['Store']] = relationship(back_populates='city')

    def __init__(self, id: str, name: str, stores: list['Store'] = None):
        self.id = id
        self.name = name
        self.stores = stores or []
