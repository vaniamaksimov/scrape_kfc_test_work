from src.crud.base import CrudBase
from src.models.feature import StoreFeature
from src.schemas.store_feature import StoreFeatureCreate, StoreFeatureUpdate


class StoreFeatureCrud(CrudBase[StoreFeature, StoreFeatureCreate, StoreFeatureUpdate]):
    ...


store_feature_crud = StoreFeatureCrud(StoreFeature)
