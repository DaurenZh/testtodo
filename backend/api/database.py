import aiosqlite
import os

DATABASE_PATH = "data/todo.db"

async def init_db():
    """Инициализация базы данных"""
    # Создаем папку data если не существует
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                done BOOLEAN DEFAULT 0
            )
        """)
        await db.commit()
        print(f"Database initialized at {DATABASE_PATH}")

async def get_db():
    """Получение подключения к базе данных"""
    db = await aiosqlite.connect(DATABASE_PATH)
    db.row_factory = aiosqlite.Row
    return db
