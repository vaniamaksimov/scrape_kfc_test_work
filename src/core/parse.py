import asyncio
from http import HTTPStatus

import requests
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.session import AsyncSessionLocal
from src.crud import city_crud, feature_crud, store_crud, store_feature_crud
from src.models.feature import Feature
from src.schemas.city import CityCreate
from src.schemas.feature import FeatureCreate
from src.schemas.kfc_json import KfcJson, ResultJson
from src.schemas.store import StoreCreate, StoreUpdate
from src.schemas.store_feature import StoreFeatureCreate
from src.utils import exceptions

url = 'https://api.kfc.digital/api/store/v2/store.get_restaurants?showClosed=true'
headers = {
    'User-Agent': (
        'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/114.0.0.0 Mobile Safari/537.36'
    )
}


def _get_response() -> requests.Response:
    response = requests.get(url=url, headers=headers)
    response.encoding = 'utf-8'
    if response.status_code != HTTPStatus.OK:
        raise exceptions.ResponseError(
            'Ну удалось получить ответ от '
            f'сервера: статус ответа {response.status_code}'
        )
    return response


def _get_data(response: requests.Response) -> dict:
    return response.json()


def _map_data_to_pydantic_model(data: dict) -> KfcJson:
    return KfcJson(**data)


async def _add_to_db(data: ResultJson) -> None:
    async with AsyncSessionLocal() as session:
        session: AsyncSession
        city = await city_crud.get(session, id=data.storePublic.kfcCityId)
        if not city:
            city = await city_crud.create(
                session, CityCreate(name=data.storePublic.contacts.city.ru)
            )

        store_features: list[Feature] = []
        for feature_name in data.storePublic.features:
            feature = await feature_crud.get(session, name=feature_name)
            if not feature:
                feature = await feature_crud.create(
                    session, FeatureCreate(name=feature_name)
                )
            store_features.append(feature)

        store = await store_crud.get(session, id=data.storePublic.storeId)
        if not store:
            store = await store_crud.create(
                session,
                StoreCreate(
                    id=data.storePublic.storeId,
                    name=data.storePublic.title.ru,
                    address=data.storePublic.contacts.streetAddress,
                    city_id=city.id,
                    longitude=data.storePublic.contacts.coordinates.geometry.coordinates[
                        0
                    ],
                    latitude=data.storePublic.contacts.coordinates.geometry.coordinates[
                        1
                    ],
                    start_time_local=data.storePublic.openingHours.regular.startTimeLocal,
                    end_time_local=data.storePublic.openingHours.regular.endTimeLocal,
                    time_zone=data.storePublic.timeZone,
                    status=data.storePublic.status,
                ),
            )
        else:
            store = await store_crud.update(
                session,
                store,
                StoreUpdate(
                    name=data.storePublic.title.ru,
                    address=data.storePublic.contacts.streetAddress,
                    city_id=city.id,
                    longitude=data.storePublic.contacts.coordinates.geometry.coordinates[
                        0
                    ],
                    latitude=data.storePublic.contacts.coordinates.geometry.coordinates[
                        1
                    ],
                    start_time_local=data.storePublic.openingHours.regular.startTimeLocal,
                    end_time_local=data.storePublic.openingHours.regular.endTimeLocal,
                    time_zone=data.storePublic.timeZone,
                    status=data.storePublic.status,
                ),
            )
            for store_feature in await store.awaitable_attrs.store_features:
                await session.delete(store_feature)
        for feature in store_features:
            await store_feature_crud.create(
                session, StoreFeatureCreate(store_id=store.id, feature_id=feature.id)
            )


async def _save_to_database(model: KfcJson) -> None:
    coros = [_add_to_db(data) for data in model.searchResults]
    await asyncio.gather(*coros)


def parse():
    response = _get_response()
    data = _get_data(response)
    model = _map_data_to_pydantic_model(data)
    asyncio.run(_save_to_database(model))
