import os
import asyncpg
from typing import Optional

DATABASE_URL = os.getenv("POSTGRES_URL")
pool: Optional[asyncpg.Pool] = None

async def init_db():
    """Инициализация базы данных"""
    global pool
    
    if not DATABASE_URL:
        raise ValueError("POSTGRES_URL environment variable is not set")
    
    try:
        # Создаем connection pool
        pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)
        
        # Создаем таблицу если не существует
        async with pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS todos (
                    id SERIAL PRIMARY KEY,
                    task TEXT NOT NULL,
                    done BOOLEAN DEFAULT FALSE
                )
            """)
        
        print("PostgreSQL database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise

async def get_db():
    """Получение соединения из pool"""
    if pool is None:
        await init_db()
    return await pool.acquire()

async def close_db():
    """Закрытие connection pool"""
    global pool
    if pool:
        await pool.close()
        pool = None
        print("Database pool closed")
