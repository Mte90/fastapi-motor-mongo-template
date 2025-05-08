import pytest
from app.db import get_db
from uuid import UUID

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name, expected_status",
    [
        (None, 422),
        ('John Doe', 201)
    ]
)
async def test_create_sample_resource(
    client, override_get_db, clear_db, name: str, expected_status: int
):
    req_json = {}
    if name is not None:
        req_json["name"] = name

    resp = await client.post(
        '/api/sample-resource-app/v1/sample-resource',
        json=req_json
    )

    assert resp.status_code == expected_status

    if 201 == expected_status:
        assert 'id' in resp.json()
        resource_id = resp.json().get('id')

        db = await get_db()
        resource_db = await db['test_db']['sample_resource'].find_one({"_id": UUID(resource_id)})
        assert resource_db.get('name') == name
        assert not resource_db.get('deleted')
