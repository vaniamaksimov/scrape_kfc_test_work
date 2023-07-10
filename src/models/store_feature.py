from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.base import Base

if TYPE_CHECKING:
    from src.models.feature import Feature
    from src.models.store import Store


class StoreFeature(Base):
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'), primary_key=True)
    feature_id: Mapped[int] = mapped_column(ForeignKey('feature.id'), primary_key=True)

    store: Mapped['Store'] = relationship(back_populates='store_features')
    feature: Mapped['Feature'] = relationship(back_populates='feature_stores')

    def __init__(self, store_id: int, feature_id: int):
        self.store_id = store_id
        self.feature_id = feature_id
