from src.crud.base import CrudBase
from src.models.store import Store
from src.schemas.store import StoreCreate, StoreUpdate


class StoreCrud(CrudBase[Store, StoreCreate, StoreUpdate]):
    ...


store_crud = StoreCrud(Store)
