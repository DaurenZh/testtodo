import uvicorn
import sys
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Добавляем текущую директорию в PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("Starting Todo API server...")
    print(f"Working directory: {os.getcwd()}")
    print(f"POSTGRES_URL: {os.getenv('POSTGRES_URL', 'Not set')[:30]}...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True, log_level="info")