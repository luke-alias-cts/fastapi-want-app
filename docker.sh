docker build -t fastapi-app .
docker run -d --name fastapi-app-container -p 8000:8000 --env-file .env.docker fastapi-app