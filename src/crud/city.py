from src.crud.base import CrudBase
from src.models.city import City
from src.schemas.city import CityCreate, CityUpdate


class CityCrud(CrudBase[City, CityCreate, CityUpdate]):
    ...


city_crud = CityCrud(City)
