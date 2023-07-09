from src.crud.base import CrudBase
from src.models.feature import Feature
from src.schemas.feature import FeatureCreate, FeatureUpdate


class FeatureCrud(CrudBase[Feature, FeatureCreate, FeatureUpdate]):
    ...


feature_crud = FeatureCrud(Feature)
