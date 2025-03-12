from sqlalchemy import or_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app import models


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
