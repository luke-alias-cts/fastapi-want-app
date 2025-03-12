FROM python:3.13.1

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install system dependencies (including netcat)
RUN apt-get update && apt-get install -y netcat-openbsd

# Copy the application into the container.
COPY . /app

# Install the application dependencies.
WORKDIR /app
RUN uv venv 
RUN uv sync --frozen --no-cache

# entrypoint 스크립트 복사 및 실행 권한 부여
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Run the application.
CMD ["/app/entrypoint.sh"]