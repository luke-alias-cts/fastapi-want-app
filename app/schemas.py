from pydantic import BaseModel
from typing import List, Optional


class TagBase(BaseModel):
    tag_name_ko: Optional[str] = None
    tag_name_en: Optional[str] = None
    tag_name_ja: Optional[str] = None


class Tag(TagBase):
    id: int

    class Config:
        orm_mode = True


class TagCreate(TagBase):
    pass


class CompanyBase(BaseModel):
    company_name_ko: Optional[str] = None
    company_name_en: Optional[str] = None
    company_name_ja: Optional[str] = None


class CompanyCreate(CompanyBase):
    pass


class Company(CompanyBase):
    id: int
    tags: List[Tag] = []

    class Config:
        orm_mode = True
