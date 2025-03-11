from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(
        title="Wanted FastAPI Project",
        description="원티드 과제 CTSICTAI",
        version="0.1",
    )
    return app


# FastAPI instance
app = create_app()


@app.get("/")
def read_root():
    return {"Hello": "World"}
