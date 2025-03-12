"""first

Revision ID: 8078a768ef82
Revises:
Create Date: 2025-03-12 11:22:20.149103

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8078a768ef82"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "companies",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("company_name_ko", sa.String(), unique=True, nullable=True),
        sa.Column("company_name_en", sa.String(), unique=True, nullable=True),
        sa.Column("company_name_ja", sa.String(), unique=True, nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "tags",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("tag_name_ko", sa.String(), unique=True, nullable=True),
        sa.Column("tag_name_en", sa.String(), unique=True, nullable=True),
        sa.Column("tag_name_ja", sa.String(), unique=True, nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "company_tag_association",
        sa.Column(
            "company_id",
            sa.Integer(),
            sa.ForeignKey("companies.id"),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "tag_id",
            sa.Integer(),
            sa.ForeignKey("tags.id"),
            primary_key=True,
            nullable=False,
        ),
    )
    pass


def downgrade() -> None:
    op.drop_table("tags")
    op.drop_table("companies")
    op.drop_table("company_tag_association")
    pass
