from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.databases import engine, meta


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 애플리케이션 시작 시 DB 테이블 생성
    async with engine.begin() as conn:
        await conn.run_sync(meta.create_all)
    yield
    # 애플리케이션 종료 시 DB 연결 해제 등 종료 작업
    await engine.dispose()


# FastAPI instance
app = FastAPI(
    title="Wanted FastAPI Project",
    description="원티드 과제 CTSICTAI",
    version="0.1",
    lifespan=lifespan,
)


@app.get("/")
async def read_root():
    return {"Hello": "World"}
