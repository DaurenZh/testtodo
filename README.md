# Todo App

Todo App - это микросервисное приложение, состоящее из двух независимых сервисов:
- **Backend** - RESTful API на FastAPI
- **Frontend** - SPA на Vue.js

## Запуск

### Вариант 1: Docker 

**Требования:**
- Docker Desktop

**Запуск:**
```bash
# Запустить приложение
docker-compose up -d --build

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down
```

**Доступ:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8001
- API Documentation: http://localhost:8001/docs

### Вариант 2: Локальный запуск

**Требования:**
- Python 3.12+
- Node.js 20+
- npm

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python main.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Функциональность

### Основные возможности:
- **Создание задач** - добавление новых todo с описанием
- **Изменение статуса** - отметка задач как выполненных/невыполненных
- **Удаление задач** - удаление ненужных задач
- **Адаптивный интерфейс** - работает на всех устройствах
- **Сохранение данных** - все данные хранятся в SQLite базе

### API Endpoints:
GET    /api/           - Получить все задачи

POST   /api/           - Создать новую задачу

PUT    /api/{id}       - Обновить задачу

DELETE /api/{id}       - Удалить задачу

GET    /               - Статус API

GET    /health         - Health check

GET    /docs           - Swagger документация

## Архитектурные решения

1. **База данных: SQLite + aiosqlite**

Почему:

Простота развертывания - не требует отдельного сервера БД
Асинхронная работа через aiosqlite
Достаточно для небольших приложений
Файловое хранилище - легко бэкапить и переносить

Альтернатива: Изначально использовался Tortoise ORM, но из-за проблем совместимости версий был заменен на прямую работу с aiosqlite.

2. **Backend: FastAPI**

Почему:

Автоматическая генерация OpenAPI документации
Встроенная валидация через Pydantic
Type hints и современный Python код
Легкое тестирование

Структура:

Разделение по слоям: routes - schemas - database
Async/await для всех операций с БД
CORS middleware для работы с frontend
Health checks для мониторинга

3. **Frontend: Vue.js 3 + Composition API**

Почему:

Реактивность из коробки
Легковесность по сравнению с React/Angular
Composition API - более гибкая организация логики
Vite для быстрой разработки

Особенности:

Single File Components - вся логика в одном файле
Reactive state через ref() и reactive()
Async/await для API запросов
Error handling для всех операций

4. **Docker & Docker Compose**

Почему:

Изоляция окружения
Одинаковая работа на всех платформах
Простое развертывание
Масштабируемость

5. **API Design: RESTful**

Принципы:

Использование HTTP методов по назначению (GET, POST, PUT, DELETE)
Статус коды: 200 (OK), 404 (Not Found), 422 (Validation Error)
JSON для всех запросов/ответов
Валидация на уровне Pydantic схем

6. **Error Handling**

**Backend:**

HTTPException для пользовательских ошибок
Автоматическая валидация через Pydantic
Try-catch блоки для работы с БД

**Frontend:**

Try-catch для всех fetch запросов
Console.error для отладки
Graceful degradation - приложение не падает при ошибках

## Технологический стек

### Backend:
FastAPI 0.104.1 - Web framework
Uvicorn 0.24.0 - ASGI server
aiosqlite 0.19.0 - Async SQLite
Pydantic 2.5.0 - Валидация данных

### Frontend:
Vue.js 3.4.0 - UI framework
Vite 5.0.0 - Build tool
Native Fetch API - HTTP клиент

### DevOps:
Docker - Контейнеризация
Docker Compose - Оркестрация

## Возможные улучшения

### Backend:

Добавить аутентификацию (JWT)
Миграции БД (Alembic)
Кэширование (Redis)
Пагинация для больших списков
Logging система

### Frontend:

State management (Pinia)
Фильтрация и сортировка задач
Drag & drop для приоритетов
Уведомления (toast)
Offline mode (PWA)

### DevOps:

CI/CD pipeline
Automated tests
Monitoring (Prometheus)
Production Docker images
