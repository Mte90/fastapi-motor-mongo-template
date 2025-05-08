import pytest


@pytest.mark.asyncio
async def test_health(client):
    resp = await client.get('/health')
    assert 200 == resp.status_code
