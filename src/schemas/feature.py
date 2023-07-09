from pydantic import BaseModel, ConfigDict, Extra


class FaetureBase(BaseModel):
    model_config = ConfigDict(extra=Extra.forbid)


class FeatureCreate(FaetureBase):
    name: str


class FeatureUpdate(FaetureBase):
    name: str | None


class FeatureDB(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
