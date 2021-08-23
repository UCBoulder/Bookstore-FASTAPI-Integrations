FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim
LABEL org.opencontainers.image.source https://github.com/UCBoulder/Bookstore-FASTAPI-Integrations

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY ./app /app/app
