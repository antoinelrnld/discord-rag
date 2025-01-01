FROM python:3.10-slim-bullseye

WORKDIR /app

RUN pip install poetry

COPY api /app/api
COPY packages/utils/ /app/packages/utils

WORKDIR /app/packages/utils
RUN poetry build

WORKDIR /app/api
RUN poetry install

# Run the API
CMD ["poetry", "run", "python", "src/api/main.py"]