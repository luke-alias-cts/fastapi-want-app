import pytest


@pytest.mark.asyncio
def test_search_companies(client):
    company_name_ko = "원티드"
    response = client.get(f"/companies/search/by-name?name={company_name_ko}")
    assert response.status_code == 200
    data1 = response.json().get("items")
    filtered = [
        item for item in data1 if item and item.get("company_name_ko") == "원티드랩"
    ]

    assert any(filtered)

    company_name_en = "wanted"
    response = client.get(f"/companies/search/by-name?name={company_name_en}")
    assert response.status_code == 200
    data2 = response.json().get("items")
    filtered = [
        item for item in data2 if item and item.get("company_name_ko") == "원티드랩"
    ]

    assert any(filtered)

    company_name_ja = "ウォンテッド"
    response = client.get(f"/companies/search/by-name?name={company_name_ja}")
    assert response.status_code == 200
    data3 = response.json().get("items")
    filtered = [
        item for item in data3 if item and item.get("company_name_ko") == "원티드랩"
    ]
    assert any(filtered)


@pytest.mark.asyncio
def test_search_companies_by_tag(client):
    tag_name_ko = "태그_3"
    response = client.get(f"/companies/search/by-tag?tag={tag_name_ko}")
    assert response.status_code == 200
    data1 = response.json().get("items")
    filtered = [
        item for item in data1 if item and item.get("company_name_ko") == "테스트회사"
    ]
    assert any(filtered)

    tag_name_en = "tag_3"
    response = client.get(f"/companies/search/by-tag?tag={tag_name_en}")
    assert response.status_code == 200
    data2 = response.json().get("items")
    filtered2 = [
        item for item in data2 if item and item.get("company_name_ko") == "테스트회사"
    ]
    assert any(filtered2)

    tag_name_ja = "タグ_3"
    response = client.get(f"/companies/search/by-tag?tag={tag_name_ja}")
    assert response.status_code == 200
    data3 = response.json().get("items")
    filtered3 = [
        item for item in data3 if item and item.get("company_name_ko") == "테스트회사"
    ]
    assert any(filtered3)
