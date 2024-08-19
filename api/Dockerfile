FROM python:3.12-slim-bookworm

WORKDIR /app

COPY . .

RUN pip3 --no-cache-dir install -r ./requirements.txt

CMD [ "uvicorn", "app:app", "--reload", "--host", "0.0.0.0", "--port", "8000" ]