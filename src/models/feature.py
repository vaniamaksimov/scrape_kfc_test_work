from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.base import Base
from src.core.settings import settings

if TYPE_CHECKING:
    from src.models.store import Store


class StoreFeature(Base):
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'), primary_key=True)
    feature_id: Mapped[int] = mapped_column(ForeignKey('feature.id'), primary_key=True)

    store: Mapped['Store'] = relationship(back_populates='store_features')
    feature: Mapped['Feature'] = relationship(back_populates='feature_stores')


class Feature(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(
        String(settings.app.max_string_length), unique=True
    )

    feature_stores: Mapped[list['StoreFeature']] = relationship(
        back_populates='feature'
    )

    def __init__(self, name: str, feature_stores: list['StoreFeature'] = None):
        self.name = name
        feature_stores = feature_stores or []
