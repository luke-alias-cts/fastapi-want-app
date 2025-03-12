import pytest


@pytest.mark.asyncio
def test_add_tag(client):
    response = client.post("/tags/companies/1", json={"tag_name_en": "tag_1424222"})
    assert response.status_code == 200
    data = response.json()
    assert data.get("id") == 1
    assert any(
        [tag for tag in data.get("tags") if tag.get("tag_name_en") == "tag_1424222"]
    )


@pytest.mark.asyncio
def test_delete_tag(client):
    response = client.delete("/tags/companies/1/1")
    assert response.status_code == 200
    data = response.json()
    assert data.get("id") == 1
    assert [tag for tag in data.get("tags") if tag.get("tag_name_en") == "tag_1"] == []
