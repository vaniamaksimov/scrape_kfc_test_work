from pydantic import BaseModel, ConfigDict, Extra


class StoreFeatureBase(BaseModel):
    model_config = ConfigDict(extra=Extra.forbid)


class StoreFeatureCreate(StoreFeatureBase):
    store_id: int
    feature_id: int


class StoreFeatureUpdate(StoreFeatureBase):
    store_id: int | None
    feature_id: int | None


class StoreFeatureDB(BaseModel):
    store_id: int
    feature_id: int

    model_config = ConfigDict(from_attributes=True)
