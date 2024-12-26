FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl && apt-get clean

WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:${PATH}"

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-dev

COPY . .

EXPOSE 9094

CMD ["poetry", "run", "gunicorn", "src.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:9094"]