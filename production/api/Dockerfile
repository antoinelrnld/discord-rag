FROM python:3.10-slim-bullseye

WORKDIR /opt/discord-rag/app

RUN pip install --no-cache-dir uv 

COPY ./production/api/pyproject.toml ./production/api/uv.lock ./
COPY ./production/api/src ./src
COPY ./packages/utils ../../packages/utils

RUN uv sync --frozen

ENV PATH="/opt/discord-rag/app/.venv/bin:$PATH"

CMD ["python", "-m", "api"]