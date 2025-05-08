from uuid import uuid4, UUID
from datetime import datetime
import logging
from pymongo import ReturnDocument
from bson import Binary

from app.conf.config import Config
from app.db.db import AsyncIOMotorClient
from app.schemas.sample_resource_common import SampleResource
from app.common.util import mask_uuid


__db_name = Config.app_settings.get('db_name')
__db_collection = 'sample_resource'

async def create_sample_resource(
    conn: AsyncIOMotorClient,
    name: str
) -> SampleResource:
    id = uuid4()
    new_sample_resource = SampleResource(
        id=id,
        name=name,
        create_time=datetime.now(),
        update_time=datetime.now(),
        deleted=False,
    )

    logging.info(
        f'Inserting sample resource {name}, {mask_uuid(id)} into db...'
    )
    await conn[__db_name][__db_collection].insert_one(
        new_sample_resource.get_json_for_mongo()
    )

    logging.info(
        f"Sample resource {name} has inserted into {__db_name}/{__db_collection}"
    )

    return new_sample_resource


async def get_sample_resource_by_id(
    conn: AsyncIOMotorClient,
    resource_id: UUID
) -> SampleResource | None:
    logging.info(f"Getting sample resource {mask_uuid(resource_id)}...")
    sample_resource = await conn[__db_name][__db_collection].find_one(
        {"$and": [
            {'_id': Binary.from_uuid(resource_id)},
            {'deleted': False},
        ]},
    )
    if sample_resource is None:
        logging.info(f"Resource {mask_uuid(resource_id)} is None")
    return sample_resource


async def update_sample_resource(
    conn: AsyncIOMotorClient,
    resource_id: UUID,
    resource_data: dict
) -> SampleResource | None:
    logging.info(
        f'Updating sample resource {mask_uuid(str(resource_id))}... in {__db_name}/{__db_collection}'
    )

    sample_resource = \
        await conn[__db_name][__db_collection].find_one_and_update(
            {"$and": [
                {'_id': Binary.from_uuid(resource_id)},
                {'deleted': False},
            ]},
            {'$set': {
                **resource_data,
                "update_time": datetime.now(),
            }},
            return_document=ReturnDocument.AFTER,
        )

    if None is sample_resource:
        logging.error(
            f"Sample resource {mask_uuid(str(resource_id))} not exist"
        )
        raise RuntimeError("Error while update sample_resource")
    else:
        logging.info(
            f'Sample resource {mask_uuid(str(resource_id))} updated'
        )
    return sample_resource


async def delete_sample_resource(
    conn: AsyncIOMotorClient,
    resource_id: UUID,
) -> SampleResource | None:
    logging.info(
        f"Deleting sample resource {mask_uuid(str(resource_id))}..."
    )

    sample_resource = await conn[__db_name][__db_collection].\
        find_one_and_update(
        {"$and": [
            {'_id': Binary.from_uuid(resource_id)},
            {'deleted': False},
        ]},
        {'$set': {
            "deleted": True,
            "update_time": datetime.now(),
        }},
        return_document=ReturnDocument.AFTER,
    )

    if None is sample_resource:
        logging.error(
            f"Sample resource {mask_uuid(str(resource_id))} not exist"
        )
        raise RuntimeError("Error while deleting sample resource")
    else:
        logging.info(
            f'Sample resource {mask_uuid(str(resource_id))} deleted'
        )
    return sample_resource
