from pydantic import BaseModel, ConfigDict, Extra


class CityBase(BaseModel):
    model_config = ConfigDict(extra=Extra.forbid)


class CityCreate(CityBase):
    id: str
    name: str


class CityUpdate(CityBase):
    name: str | None


class CityDB(BaseModel):
    id: str
    name: str

    model_config = ConfigDict(from_attributes=True)
