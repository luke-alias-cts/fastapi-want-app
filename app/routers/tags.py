from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas
from app.databases import get_db

router = APIRouter(prefix="/tags", tags=["tags"])


@router.post("/companies/{company_id}", response_model=schemas.Company)
async def add_tag(
    company_id: int, tag: schemas.TagCreate, db: AsyncSession = Depends(get_db)
):
    company = await crud.add_tag_to_company(db, company_id, tag)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.delete("/companies/{company_id}/{tag_id}", response_model=schemas.Company)
async def delete_tag(company_id: int, tag_id: int, db: AsyncSession = Depends(get_db)):
    company = await crud.remove_tag_from_company(db, company_id, tag_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company or Tag not found")
    return company
