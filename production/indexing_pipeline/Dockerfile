FROM python:3.10-slim-bullseye

WORKDIR /app

RUN pip install poetry

COPY indexing_pipeline /app/indexing_pipeline
COPY packages/utils/ /app/packages/utils

WORKDIR /app/packages/utils
RUN poetry build

WORKDIR /app/indexing_pipeline
RUN poetry install

# Run the indexing pipeline
CMD ["poetry", "run", "python", "src/indexing_pipeline/main.py"]