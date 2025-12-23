from fastapi import APIRouter, HTTPException
from api.schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from api.database import get_db
from typing import List

todo_router = APIRouter(tags=["todo"])

@todo_router.get("/", response_model=List[TodoResponse])
async def get_todos():
    conn = await get_db()
    try:
        rows = await conn.fetch("SELECT * FROM todos ORDER BY id")
        return [dict(row) for row in rows]
    finally:
        await conn.close()

@todo_router.post("/", response_model=TodoResponse)
async def create_todo(todo: TodoCreate):
    conn = await get_db()
    try:
        row = await conn.fetchrow(
            "INSERT INTO todos (task, done) VALUES ($1, $2) RETURNING *",
            todo.task, todo.done
        )
        return dict(row)
    finally:
        await conn.close()

@todo_router.put("/{id}", response_model=TodoResponse)
async def update_todo(id: int, todo: TodoUpdate):
    conn = await get_db()
    try:
        existing = await conn.fetchrow("SELECT * FROM todos WHERE id = $1", id)
        if not existing:
            raise HTTPException(status_code=404, detail="Todo not found")
            
        update_data = todo.model_dump(exclude_unset=True)
        if not update_data:
            return dict(existing)
        
        # Строим UPDATE запрос
        set_parts = []
        values = []
        param_count = 1
        
        for key, value in update_data.items():
            set_parts.append(f"{key} = ${param_count}")
            values.append(value)
            param_count += 1
        
        values.append(id)
        query = f"UPDATE todos SET {', '.join(set_parts)} WHERE id = ${param_count} RETURNING *"
        
        row = await conn.fetchrow(query, *values)
        return dict(row)
    finally:
        await conn.close()

@todo_router.delete("/{id}")
async def delete_todo(id: int):
    conn = await get_db()
    try:
        existing = await conn.fetchrow("SELECT * FROM todos WHERE id = $1", id)
        if not existing:
            raise HTTPException(status_code=404, detail="Todo not found")
        
        await conn.execute("DELETE FROM todos WHERE id = $1", id)
        return {"detail": "Todo deleted successfully"}
    finally:
        await conn.close()