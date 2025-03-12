from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.databases import sessionmanager
from app.config import config
from app.routers import companies, tags
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware


def init_app(init_db=True):
    if init_db:
        sessionmanager.init(config.SQLALCHEMY_DATABASE_URI, {"echo": config.ECHO_SQL})

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            yield
            if sessionmanager._engine is not None:
                await sessionmanager.close()
    else:
        return None


# FastAPI instance
def create_app(init_db=True):
    app = FastAPI(
        title="Wanted FastAPI Project",
        description="원티드 과제 CTSICTAI",
        version="0.1",
        lifespan=init_app(init_db),
    )
    origins = [
        "http://localhost",
        "http://localhost:8000",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # Include routers
    app.include_router(companies.router)
    app.include_router(tags.router)
    add_pagination(app)

    return app


app = create_app()
