# tests/conftest.py
import pytest
import asyncio
from contextlib import ExitStack
from fastapi.testclient import TestClient
from app.main import app as actual_app


@pytest.fixture(autouse=True)
def app():
    with ExitStack():
        yield actual_app


@pytest.fixture
def client(app):
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
