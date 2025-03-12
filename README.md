# Wanted assignment FASTAPI App 

### uv packaging manager 기반
[uv 설치 방법 - 공식문서 참조](https://docs.astral.sh/uv/getting-started/installation/)

- `uv sync --frozen --no-cache` 로 dependency package 설치

- `uv run fastapi dev`로 로컬에서 실행 가능

- `uv run pytest -s`로 test 파일 실행가능

### tech stack
- RDMS: postgresql
- migration: alembic
- ORM: Sqlalchemy
- api docs: swagger
- formatter: ruff
- IDE: vscode