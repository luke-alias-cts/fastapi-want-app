# Wanted assignment FASTAPI App 

### uv packaging manager 기반
[uv 설치 방법 - 공식문서 참조](https://docs.astral.sh/uv/getting-started/installation/)

- `uv sync --frozen --no-cache` 로 dependency package 설치

- `uv run fastapi dev`로 로컬에서 실행 가능

- `uv run pytest -s`로 test 파일 실행가능

- `uv run alembic upgrade head`로 migration 실행

### tech stack
- RDMS: postgresql
- migration: alembic
- ORM: Sqlalchemy
- api docs: swagger, [api_docs](api_docs.json) 
- formatter: ruff
- IDE: vscode

### .env variable
```
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DB_NAME=
```

### docker run
`./docker.sh`실행
<br> 단, local postgres가 있어야 가능!




