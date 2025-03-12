# tests/conftest.py
import pytest
import asyncio
from contextlib import ExitStack
from fastapi.testclient import TestClient
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor
from app.databases import sessionmanager, get_db
from app.main import create_app
from app.models import Company, Tag


@pytest.fixture(autouse=True)
def app():
    with ExitStack():
        yield create_app(init_db=False)


@pytest.fixture
def client(app):
    with TestClient(app) as c:
        yield c


test_db = factories.postgresql_proc(port=None, dbname="test_wanted_db")


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def connection_test(test_db, event_loop):
    pg_host = test_db.host
    pg_port = test_db.port
    pg_user = test_db.user
    pg_db = test_db.dbname
    pg_password = test_db.password

    with DatabaseJanitor(
        user=pg_user,
        host=pg_host,
        port=pg_port,
        dbname=pg_db,
        version=test_db.version,
        password=pg_password,
    ):
        connection_str = f"postgresql+psycopg://{pg_user}:@{pg_host}:{pg_port}/{pg_db}"
        sessionmanager.init(connection_str)
        yield
        await sessionmanager.close()


@pytest.fixture(scope="function", autouse=True)
async def create_tables(connection_test):
    async with sessionmanager.connect() as connection:
        await sessionmanager.drop_all(connection)
        await sessionmanager.create_all(connection)


@pytest.fixture(scope="function", autouse=True)
async def seed_data():
    async with sessionmanager.session() as session:
        # 시드 데이터 생성: 예시로 2개의 회사와 3개의 태그, 그리고 회사-태그 연관 설정
        company1 = Company(
            company_name_ko="원티드랩",
            company_name_en="WantedLab",
            company_name_ja="ウォンテッドラボ",
        )
        company2 = Company(
            company_name_ko="테스트회사",
            company_name_en="TestCompany",
            company_name_ja="テストカンパニー",
        )
        tag1 = Tag(tag_name_ko="태그_1", tag_name_en="tag_1", tag_name_ja="タグ_1")
        tag2 = Tag(tag_name_ko="태그_2", tag_name_en="tag_2", tag_name_ja="タグ_2")
        tag3 = Tag(tag_name_ko="태그_3", tag_name_en="tag_3", tag_name_ja="タグ_3")
        # 연관 관계 설정 (예: 회사1에는 tag1, tag2, 회사2에는 tag3)
        company1.tags = [tag1, tag2]
        company2.tags = [tag3]
        session.add_all([company1, company2, tag1, tag2, tag3])
        await session.commit()
        yield  # 테스트가 실행되는 동안 시드 데이터는 그대로 유지됨


@pytest.fixture(scope="function", autouse=True)
async def session_override(app, connection_test):
    async def get_db_override():
        async with sessionmanager.session() as session:
            yield session

    app.dependency_overrides[get_db] = get_db_override


@pytest.fixture(scope="session")
def test_connection_str(test_db):
    pg_host = test_db.host
    pg_port = test_db.port
    pg_user = test_db.user
    pg_db = test_db.dbname
    pg_password = test_db.password
    return f"postgresql+psycopg://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"
