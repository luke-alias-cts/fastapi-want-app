import pytest
from app import crud, schemas
from app.databases import sessionmanager


@pytest.mark.asyncio
async def test_get_companies_by_name():
    async with sessionmanager.session() as session:
        companies = await crud.get_companies_by_name(session, "wanted")
        result = [
            instance.__dict__
            for instance in companies
            if instance.__dict__.get("company_name_ko") == "원티드랩"
        ]
        assert any(result)


@pytest.mark.asyncio
async def test_get_companies_by_tag():
    async with sessionmanager.session() as session:
        companies = await crud.get_companies_by_tag(session, "タグ_3")
        result = [
            instance.__dict__
            for instance in companies
            if instance.__dict__.get("company_name_ja") == "テストカンパニー"
        ]
        assert any(result)

        assert any(
            tag.__dict__.get("tag_name_ja") == "タグ_3" for tag in result[0].get("tags")
        )


@pytest.mark.asyncio
async def test_add_tag_to_company_new_tag():
    async with sessionmanager.session() as session:
        company_id = 1
        tag_data = schemas.TagCreate(tag_name_en="tag_4")
        await crud.add_tag_to_company(session, company_id, tag_data)

        companies = await crud.get_companies_by_tag(session, "tag_4")
        result = [
            instance.__dict__
            for instance in companies
            if instance.__dict__.get("company_name_ko") == "원티드랩"
        ]
        assert any(result)

        assert any(
            tag.__dict__.get("tag_name_en") == "tag_4" for tag in result[0].get("tags")
        )


@pytest.mark.asyncio
async def test_add_tag_to_company_exists_tag():
    async with sessionmanager.session() as session:
        company_id = 1
        tag_data = schemas.TagCreate(tag_name_en="tag_3")
        await crud.add_tag_to_company(session, company_id, tag_data)

        companies = await crud.get_companies_by_tag(session, "tag_3")
        result = [
            instance.__dict__
            for instance in companies
            if instance.__dict__.get("company_name_ko") == "원티드랩"
        ]
        assert any(result)

        assert any(
            tag.__dict__.get("tag_name_en") == "tag_3" for tag in result[0].get("tags")
        )


@pytest.mark.asyncio
async def test_remove_tag_from_company():
    async with sessionmanager.session() as session:
        company_id = 1
        tag_id = 1
        await crud.remove_tag_from_company(session, company_id, tag_id)

        companies = await crud.get_companies_by_name(session, "wanted")

        result = [
            instance.__dict__
            for instance in companies
            if instance.__dict__.get("company_name_ko") == "원티드랩"
        ]
        assert any(result)

        assert all(
            tag.__dict__.get("tag_name_en") != "tag_1" for tag in result[0].get("tags")
        )
