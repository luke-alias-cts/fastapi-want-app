import pytest


@pytest.mark.asyncio
async def test_read_root_async(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
