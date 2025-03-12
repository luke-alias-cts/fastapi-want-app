from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas
from app.databases import get_db
from fastapi_pagination import Page, paginate

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("/search/by-name", response_model=Page[schemas.Company])
async def search_companies(name: str, db: AsyncSession = Depends(get_db)):
    companies = await crud.get_companies_by_name(db, name)
    return paginate(companies)


@router.get("/search/by-tag", response_model=Page[schemas.Company])
async def search_companies_by_tag(tag: str, db: AsyncSession = Depends(get_db)):
    companies = await crud.get_companies_by_tag(db, tag)
    return paginate(companies)
