FROM python:3.10-slim-bookworm

WORKDIR /app

RUN pip install --no-cache-dir uv 

COPY ./production/indexing_pipeline/pyproject.toml ./production/indexing_pipeline/uv.lock ./
COPY ./production/indexing_pipeline/src ./src

RUN uv sync --frozen

ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "-m", "indexing_pipeline"]