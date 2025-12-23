# Todo App

Todo App - это микросервисное приложение, состоящее из двух независимых сервисов:
- **Backend** - RESTful API на FastAPI
- **Frontend** - SPA на Vue.js

## Запуск

### Локальный запуск

**Требования:**
- Python 3.12+
- Node.js 20+
- npm

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\Activate
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
