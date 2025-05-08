import pytest
from app.db import get_db
from uuid import UUID
from app.common.error import UnprocessableError


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "resource_id, expected_status",
    [
        ("5e8e793e-b7b6-4ad0-ba78-94445ef2a286", 200),
        ("cef4485f-fed7-48e3-99c6-47da4c04a894", 200),
        ("c0a207d1-1734-4052-b127-4845eb9d40bb", 422),
        (None, 405),
    ]
)
async def test_delete_sample_resource(
    client, override_get_db, clear_db, resource_id: UUID, expected_status: int
):

    path = '/api/sample-resource-app/v1/sample-resource'
    if None is not resource_id:
        path = f'{path}/{resource_id}'

    try:
        resp = await client.delete(
            path,
        )
        assert resp.status_code == expected_status

        if 200 == resp.status_code:
            db = await get_db()
            resource_db = await db['test_db']['sample_resource'].find_one({"_id": UUID(resource_id)})
            assert True is resource_db.get('deleted')

    except UnprocessableError as e:
        assert expected_status in (200, 422)
