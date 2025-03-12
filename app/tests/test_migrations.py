import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import inspect


@pytest.fixture(scope="module")
async def test_engine(test_connection_str):
    engine = create_async_engine(test_connection_str)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="module")
def alembic_config(test_engine):
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", str(test_engine.url))
    yield config


@pytest.fixture(scope="module")
async def test_alembic_upgrade(alembic_config, test_engine):
    command.upgrade(alembic_config, "head")

    async with test_engine.connect() as conn:

        def get_tables(sync_conn):
            insp = inspect(sync_conn)
            return insp.get_table_names()

        tables = await conn.run_sync(get_tables)

    expected_tables = ["companies", "tags", "company_tag_association"]

    for table in expected_tables:
        assert table in tables, f"Migration 후 '{table}' 테이블이 존재해야 합니다."
