FROM python:3.12
WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry config virtualenvs.create false && poetry install

COPY ./app /app
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

CMD ["./wait-for-it.sh", "db:5432", "--", "poetry", "run", "uvicorn", "app.main:main_app", "--host", "0.0.0.0", "--port", "8000"]
