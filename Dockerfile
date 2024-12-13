FROM python:3.12

WORKDIR /github/workspace

RUN pip install poetry
COPY poetry.lock pyproject.toml .
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY . .

ENTRYPOINT ["/github/workspace/entrypoint.sh"]
