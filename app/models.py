from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.databases import Base

# 회사와 태그 간 N:M 관계를 위한 association 테이블
company_tag_association = Table(
    "company_tag_association",
    Base.metadata,
    Column("company_id", Integer, ForeignKey("companies.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    company_name_ko = Column(String, nullable=True)
    company_name_en = Column(String, nullable=True)
    company_name_ja = Column(String, nullable=True)

    # 다대다 관계: 한 회사가 여러 태그를 가질 수 있음
    tags = relationship(
        "Tag",
        secondary=company_tag_association,
        back_populates="companies",
        lazy="selectin",
    )


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    tag_name_ko = Column(String, unique=True, index=True, nullable=True)
    tag_name_en = Column(String, unique=True, index=True, nullable=True)
    tag_name_ja = Column(String, unique=True, index=True, nullable=True)

    companies = relationship(
        "Company", secondary=company_tag_association, back_populates="tags"
    )
