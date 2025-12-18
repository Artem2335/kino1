# 🚀 Руководство Миграции (Migration Guide)

## ⚠️ Важно: Обновлены эндпоинты API

Если вы пишете **фронтенд** для этого проекта, внимательно прочитайте этот файл!

## До Обновления (OLD - НЕПРАВИЛЬНО) ❌

### Reviews в Movies

```javascript
// ❌ ЭТИ ЗАПРОСЫ БОЛЬШЕ НЕ РАБОТАЮТ
GET  /api/movies/1/reviews
POST /api/movies/1/reviews
DELETE /api/movies/1/reviews/100
```

### Favorites в Movies

```javascript
// ❌ ЭТИ ЗАПРОСЫ БОЛЬШЕ НЕ РАБОТАЮТ
POST /api/movies/1/favorites
DELETE /api/movies/1/favorites
GET /api/movies/user/1/favorites
```

## После Обновления (NEW - ПРАВИЛЬНО) ✅

### Reviews - Отдельный эндпоинт

```javascript
// ✅ ИСПОЛЬЗУЙТЕ ЭТИ ЗАПРОСЫ

// Получить все отзывы (для админа)
GET /api/reviews

// Получить один отзыв по ID
GET /api/reviews/100

// Получить отзывы конкретного фильма
GET /api/reviews/movie/1

// Создать отзыв
POST /api/reviews
Body: {
  "movie_id": 1,
  "text": "Отличный фильм!",
  "rating": 5
}

// Обновить отзыв (только автор или админ)
PUT /api/reviews/100
Body: {
  "text": "Хм, размышлял дальше...",
  "rating": 4
}

// Удалить отзыв (только автор или админ)
DELETE /api/reviews/100
```

### Favorites - Отдельный эндпоинт

```javascript
// ✅ ИСПОЛЬЗУЙТЕ ЭТИ ЗАПРОСЫ

// Получить мои избранные фильмы (требует авторизация)
GET /api/favorites
Headers: {
  "Authorization": "Bearer <token>"
}

// Добавить фильм в избранное
POST /api/favorites/1
Headers: {
  "Authorization": "Bearer <token>"
}

// Удалить фильм из избранного
DELETE /api/favorites/1
Headers: {
  "Authorization": "Bearer <token>"
}
```

### Movies - Остался на месте ✅

```javascript
// ✅ ОСТАЕТСЯ БЕЗ ИЗМЕНЕНИЙ

// Получить все фильмы
GET /api/movies
// Параметры: ?genre=Action&sort=year

// Получить статистику
GET /api/movies/stats

// Получить один фильм
GET /api/movies/1

// Создать фильм (админ)
POST /api/movies
Body: {
  "title": "Новый фильм",
  "description": "Описание",
  "genre": "Action",
  "year": 2024,
  "poster_url": "https://example.com/poster.jpg"
}

// Обновить фильм (админ)
PUT /api/movies/1
Body: { /* поля для обновления */ }

// Удалить фильм (админ)
DELETE /api/movies/1

// Получить рейтинг фильма
GET /api/movies/1/rating-stats
```

## 🔄 Быстрая Таблица Преобразования

| Старый Запрос | Новый Запрос | Статус |
|------|------|--------|
| `GET /api/movies/1/reviews` | `GET /api/reviews/movie/1` | 🔄 |
| `POST /api/movies/1/reviews` | `POST /api/reviews` | 🔄 |
| `DELETE /api/movies/{id}/reviews/{rev_id}` | `DELETE /api/reviews/{rev_id}` | 🔄 |
| `POST /api/movies/1/favorites` | `POST /api/favorites/1` | 🔄 |
| `DELETE /api/movies/1/favorites` | `DELETE /api/favorites/1` | 🔄 |
| `GET /api/movies/user/1/favorites` | `GET /api/favorites` | 🔄 |
| `GET /api/movies` | `GET /api/movies` | ✅ |
| `GET /api/movies/1` | `GET /api/movies/1` | ✅ |

## 📝 Примеры Для разных Языков

### JavaScript / Fetch

```javascript
// Получить отзывы фильма
fetch('/api/reviews/movie/1')
  .then(r => r.json())
  .then(data => console.log(data));

// Создать отзыв
fetch('/api/reviews', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    movie_id: 1,
    text: 'Отличный фильм!',
    rating: 5
  })
});

// Добавить в избранное
fetch('/api/favorites/1', {
  method: 'POST',
  headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
});
```

### Python / Requests

```python
import requests

# Получить отзывы
response = requests.get('http://localhost:8000/api/reviews/movie/1')
print(response.json())

# Создать отзыв
requests.post('http://localhost:8000/api/reviews', json={
    'movie_id': 1,
    'text': 'Отличный фильм!',
    'rating': 5
})

# Добавить в избранное
requests.post('http://localhost:8000/api/favorites/1',
    headers={'Authorization': 'Bearer YOUR_TOKEN'})
```

### cURL

```bash
# Получить отзывы фильма
curl http://localhost:8000/api/reviews/movie/1

# Создать отзыв
curl -X POST http://localhost:8000/api/reviews \
  -H "Content-Type: application/json" \
  -d '{
    "movie_id": 1,
    "text": "Отличный фильм!",
    "rating": 5
  }'

# Добавить в избранное
curl -X POST http://localhost:8000/api/favorites/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🛠️ Обновление Вашего Frontend кода

### Vue.js / React

```javascript
// ❌ СТАРО
const getReviews = (movieId) => 
  fetch(`/api/movies/${movieId}/reviews`)

// ✅ НОВОЕ  
const getReviews = (movieId) => 
  fetch(`/api/reviews/movie/${movieId}`)

// ❌ СТАРО
const addToFavorites = (movieId) => 
  fetch(`/api/movies/${movieId}/favorites`, {method: 'POST'})

// ✅ НОВОЕ
const addToFavorites = (movieId) => 
  fetch(`/api/favorites/${movieId}`, {method: 'POST'})
```

## ✅ Тестирование После Обновления

### 1. Проверить Movies (не изменился)

```bash
# Должно работать как раньше
curl http://localhost:8000/api/movies
```

### 2. Проверить Reviews (новое место)

```bash
# Должно вернуть все отзывы
curl http://localhost:8000/api/reviews

# Должно вернуть отзывы фильма
curl http://localhost:8000/api/reviews/movie/1
```

### 3. Проверить Favorites (новое место)

```bash
# Должно вернуть избранные
curl http://localhost:8000/api/favorites
```

### 4. Проверить, что старые пути НЕ работают

```bash
# Должно вернуть 404
curl http://localhost:8000/api/movies/1/reviews
# Должно вернуть 404
curl http://localhost:8000/api/movies/1/favorites
```

## 🎯 Основные Моменты

1. **Reviews** - теперь в `/api/reviews`, не в `/api/movies/.../reviews`
2. **Favorites** - теперь в `/api/favorites`, не в `/api/movies/.../favorites`
3. **Movies** - остаются в `/api/movies` без изменений
4. **Каждый эндпоинт** - отвечает за свою ответственность

## 📚 Дополнительно

- [Полная API документация](./API_STRUCTURE.md)
- [Что изменилось](./CHANGES.md)
- [Быстрый обзор](./REFACTORING_SUMMARY.md)

## 💡 Совет для разработчиков

Если у вас есть фронтенд, использующий старые пути:

1. Найти все запросы с `/api/movies/.../reviews`
2. Заменить на `/api/reviews`
3. Найти все запросы с `/api/movies/.../favorites`
4. Заменить на `/api/favorites`
5. Тестировать!

## ❓ Если что-то не работает

1. Проверьте, что сервер запущен на порту 8000
2. Посетите http://localhost:8000/docs для интерактивной документации
3. Проверьте консоль браузера на ошибки
4. Убедитесь, что вы используете ПРАВИЛЬНЫЕ пути из этого файла

---

**Удачи с разработкой! 🎮**
