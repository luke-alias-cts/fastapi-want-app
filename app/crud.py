from sqlalchemy import or_
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app import models
from app import schemas


# 회사 이름(다국어) 검색 (자동완성 포함)
async def get_companies_by_name(db: AsyncSession, query: str):
    result = await db.execute(
        select(models.Company).filter(
            or_(
                models.Company.company_name_ko.ilike(f"%{query}%"),
                models.Company.company_name_en.ilike(f"%{query}%"),
                models.Company.company_name_ja.ilike(f"%{query}%"),
            )
        )
    )
    return result.scalars().all()


# 태그명을 기준으로 회사 검색 (동일 회사 중복 제거)
async def get_companies_by_tag(db: AsyncSession, tag_query: str):
    result = await db.execute(
        select(models.Company)
        .join(models.Company.tags)
        .filter(
            or_(
                models.Tag.tag_name_ko.ilike(f"%{tag_query}%"),
                models.Tag.tag_name_en.ilike(f"%{tag_query}%"),
                models.Tag.tag_name_ja.ilike(f"%{tag_query}%"),
            )
        )
        .distinct()
    )
    return result.scalars().all()


# 회사 태그 추가 (태그가 없으면 생성)
async def add_tag_to_company(
    db: AsyncSession, company_id: int, tag_data: schemas.TagCreate
):
    result = await db.execute(
        select(models.Company)
        .options(selectinload(models.Company.tags))
        .filter(models.Company.id == company_id)
    )
    company = result.scalar_one_or_none()
    if not company:
        return None

    conditions = []
    # 각 필드에 값이 있을 때만 조건을 추가
    if tag_data.tag_name_ko:
        conditions.append(models.Tag.tag_name_ko == tag_data.tag_name_ko)
    if tag_data.tag_name_en:
        conditions.append(models.Tag.tag_name_en == tag_data.tag_name_en)
    if tag_data.tag_name_ja:
        conditions.append(models.Tag.tag_name_ja == tag_data.tag_name_ja)

    tag = None
    if conditions:
        result_tag = await db.execute(select(models.Tag).filter(or_(*conditions)))
        tag = result_tag.scalar_one_or_none()

    if not tag:
        tag = models.Tag(**tag_data.dict())
        db.add(tag)
        await db.commit()
        await db.refresh(tag)

    # 리프레쉬 eagar loading include tags
    await db.refresh(company, attribute_names=["tags"])
    if tag not in company.tags:
        company.tags.append(tag)
        db.add(company)
        await db.commit()
        await db.refresh(company)
    return company


# 회사에서 태그 삭제
async def remove_tag_from_company(db: AsyncSession, company_id: int, tag_id: int):
    result = await db.execute(
        select(models.Company)
        # .options(selectinload(models.Company.tags))
        .filter(models.Company.id == company_id)
    )
    company = result.scalar_one_or_none()
    if not company:
        return None

    tag_to_remove = None
    for tag in company.tags:
        if tag.id == tag_id:
            tag_to_remove = tag
            break
    if tag_to_remove:
        company.tags.remove(tag_to_remove)
        db.add(company)
        await db.commit()
        await db.refresh(company)
    return company
