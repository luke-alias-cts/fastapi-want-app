import pytest


@pytest.mark.asyncio
def test_search_companies(client):
    company_name_ko = "원티드"
    response = client.get(f"/companies/search/by-name?name={company_name_ko}")
    assert response.status_code == 200

    company_name_en = "wanted"
    response = client.get(f"/companies/search/by-name?name={company_name_en}")
    assert response.status_code == 200

    company_name_ja = "ウォンテッド"
    response = client.get(f"/companies/search/by-name?name={company_name_ja}")
    assert response.status_code == 200


@pytest.mark.asyncio
def test_search_companies_by_tag(client):
    tag_name_ko = "태그_1"
    response = client.get(f"/companies/search/by-tag?tag={tag_name_ko}")
    assert response.status_code == 200

    tag_name_en = "tag_1"
    response = client.get(f"/companies/search/by-tag?tag={tag_name_en}")
    assert response.status_code == 200

    tag_name_ja = "タグ_1"
    response = client.get(f"/companies/search/by-tag?tag={tag_name_ja}")
    assert response.status_code == 200
