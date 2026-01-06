FROM python:3.10-slim-bullseye

WORKDIR /opt/discord-rag/app

RUN pip install --no-cache-dir uv 

COPY ./production/indexing_pipeline/pyproject.toml ./production/indexing_pipeline/uv.lock ./
COPY ./production/indexing_pipeline/src ./src
COPY ../../packages/utils ../../packages/utils

RUN uv sync --frozen

ENV PATH="/opt/discord-rag/app/.venv/bin:$PATH"

CMD ["python", "-m", "indexing_pipeline"]