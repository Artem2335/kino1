# API Structure Documentation

## Overview

КиноВзор API разделена на три независимых модуля с чистой архитектурой:

```
app/
├── movies/         # ручки для работы с фильмами
├── reviews/        # ручки для работы с отзывами
├── favorites/      # ручки для работы с избранным
└── ...
```

## Каждый модуль содержит:

- `router.py` - Flask/FastAPI маршруты (endpoints)
- `models.py` - ORM модели базы данных
- `schemas.py` - Pydantic схемы валидации данных
- `dao.py` - Data Access Object (работа с БД)

## API Endpoints

### Movies (Фильмы) - `/api/movies`

**Все операции CRUD для фильмов:**

```bash
GET    /api/movies              # Получить все фильмы (с фильтрацией)
GET    /api/movies/stats        # Статистика по фильмам
GET    /api/movies/{movie_id}   # Получить фильм по ID
POST   /api/movies              # Создать новый фильм (админ)
PUT    /api/movies/{movie_id}   # Обновить фильм (админ)
DELETE /api/movies/{movie_id}   # Удалить фильм (админ)
GET    /api/movies/{movie_id}/rating-stats  # Статистика рейтинга фильма
```

### Reviews (Отзывы) - `/api/reviews`

**Все операции CRUD для отзывов:**

```bash
GET    /api/reviews                    # Получить все отзывы (админ)
GET    /api/reviews/{review_id}        # Получить отзыв по ID
POST   /api/reviews                    # Создать отзыв
PUT    /api/reviews/{review_id}        # Обновить отзыв (автор)
DELETE /api/reviews/{review_id}        # Удалить отзыв (автор/админ)
GET    /api/reviews/movie/{movie_id}   # Получить отзывы фильма
```

### Favorites (Избранное) - `/api/favorites`

**Все операции для управления избранным:**

```bash
GET    /api/favorites              # Получить мои избранные фильмы
POST   /api/favorites/{movie_id}   # Добавить фильм в избранное
DELETE /api/favorites/{movie_id}   # Удалить фильм из избранного
```

## Запуск приложения

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Инициализация БД

```bash
python init_db.py
python seed_db.py
```

### 3. Запуск сервера

```bash
python run.py
```

Сервер запустится на **http://127.0.0.1:8000**

### 4. Доступные интерфейсы

- **API документация**: http://127.0.0.1:8000/docs
- **Admin панель**: http://127.0.0.1:8000/admin
- **Frontend**: http://127.0.0.1:8000

## Проблемы с портами

Если порт **8000** уже занят, отредактируйте `run.py`:

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8001,  # Измените здесь
        reload=True
    )
```

## Архитектурные решения

### Почему модули отделены?

1. **Разделение ответственности** - каждый модуль отвечает за одно
2. **Масштабируемость** - легко добавлять новые модули
3. **Тестирование** - каждый модуль тестируется независимо
4. **Читаемость** - код организован логически

### Как модули взаимодействуют?

Все модули используют общий слой `app/db.py` для работы с БД:

```python
# в любом модуле
from app import db

movie = db.get_movie_by_id(1)
reviews = db.get_movie_reviews(1)
favorites = db.get_user_favorites(user_id)
```

## Миграция и обновление

### Если нужно пересоздать БД

```bash
rm kinovzor.db              # Удалить старую БД
python init_db.py           # Создать новую
python seed_db.py           # Загрузить тестовые данные
```

### Просмотр SQL запросов

Включите дебаг режим в `app/config.py`:

```python
SQLALCHEMY_ECHO = True  # Выведет все SQL запросы в консоль
```
