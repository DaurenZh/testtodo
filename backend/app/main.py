from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.todo import todo_router
from api.database import init_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Initializing database...")
    await init_db()
    print("Database initialized!")
    yield
    # Shutdown
    print("Shutting down...")

app = FastAPI(lifespan=lifespan, title="Todo API")

# CORS настройки - разрешаем все origins для разработки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todo_router)

@app.get("/")
def index():
    return {"status": "todo API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
