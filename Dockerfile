FROM python:3.12
WORKDIR /app

# Копіюємо залежності та встановлюємо їх
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry config virtualenvs.create false && poetry install

# Копіюємо весь бекенд
COPY ./app /app

# Запускаємо FastAPI
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]