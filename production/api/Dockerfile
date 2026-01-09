FROM python:3.10-slim-bullseye

WORKDIR /app

RUN pip install --no-cache-dir uv 

COPY ./production/api/pyproject.toml ./production/api/uv.lock ./
COPY ./production/api/src ./src

RUN uv sync --frozen

ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "-m", "api"]