FROM python:3.12

RUN pip install poetry
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi
COPY . /
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]