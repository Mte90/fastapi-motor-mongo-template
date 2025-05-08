import pytest
import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient
from httpx import AsyncClient
from app.main import app
from app.db import connect_and_init_db, close_db_connect, get_db_client, get_db
from app.conf.logging import setup_logging
from httpx import AsyncClient, ASGITransport
import os
import json

setup_logging()

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def init_db():
    await connect_and_init_db()
    yield
    await close_db_connect()


@pytest.fixture
async def db_client() -> AsyncIOMotorClient:
    client = await get_db_client()
    return client


@pytest.fixture
async def db():
    database = await get_db()
    yield database


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def override_get_db(db):
    async def _override():
        yield db
    app.dependency_overrides[get_db] = _override
    yield
    app.dependency_overrides.clear()


@pytest.fixture
async def clear_db(db):
    collections = await db.list_collection_names()
    for name in collections:
        await db.drop_collection(name)
    yield

@pytest.fixture(scope="function")
async def mock_data(request):
    json_file_path = os.path.join(os.path.dirname(__file__), "mock_data/sample_resource.json")
    db = await get_db()
    await db['test_db']['sample_resource'].delete_many({})

    with open(json_file_path, 'r') as file:
        data = json.load(file)

        for i, doc in enumerate(data):
            if "_id" in doc:
                data[i]["_id"] = uuid.UUID(doc["_id"])
        await db['test_db']['sample_resource'].insert_many(data)

    return data
