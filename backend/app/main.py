from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.todo import todo_router
from api.database import init_db, close_db
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Initializing database...")
    try:
        await init_db()
        print("Database initialized!")
    except Exception as e:
        print(f"Error initializing database: {e}")
    yield
    # Shutdown
    print("Closing database...")
    try:
        await close_db()
        print("Shutdown complete")
    except Exception as e:
        print(f"Error closing database: {e}")

app = FastAPI(lifespan=lifespan, title="Todo API")

# CORS настройки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Добавляем префикс /api
app.include_router(todo_router, prefix="/api")

@app.get("/")
def index():
    return {"status": "todo API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
