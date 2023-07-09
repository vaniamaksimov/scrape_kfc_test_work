from pydantic import UUID4, BaseModel, ConfigDict, Extra


class CityBase(BaseModel):
    model_config = ConfigDict(extra=Extra.forbid)


class CityCreate(CityBase):
    name: str


class CityUpdate(CityBase):
    name: str | None


class CityDB(BaseModel):
    id: UUID4
    name: str

    model_config = ConfigDict(from_attributes=True)
