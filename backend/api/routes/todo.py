from fastapi import APIRouter, HTTPException
from api.schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from api.database import get_db
from typing import List

todo_router = APIRouter(prefix="/api", tags=["todo"])

@todo_router.get("/", response_model=List[TodoResponse])
async def get_todos():
    db = await get_db()
    try:
        async with db.execute("SELECT * FROM todos") as data:
            rows = await data.fetchall()
            return [dict(row) for row in rows]
    finally:
        await db.close()

@todo_router.post("/", response_model=TodoResponse)
async def create_todo(todo: TodoCreate):
    db = await get_db()
    try:
        cursor = await db.execute(
            "INSERT INTO todos (task, done) VALUES (?, ?)",
            (todo.task, todo.done)
        )
        await db.commit()
        todo_id = data.lastrowid
        
        async with db.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)) as data:
            row = await data.fetchone()
            return dict(row)
    finally:
        await db.close()

@todo_router.put("/{id}", response_model=TodoResponse)
async def update_todo(id: int, todo: TodoUpdate):
    db = await get_db()
    try:

        async with db.execute("SELECT * FROM todos WHERE id = ?", (id,)) as data:
            existing = await data.fetchone()
            if not existing:
                raise HTTPException(status_code=404, detail="Todo not found")
            
        update_data = todo.dict(exclude_unset=True)
        if not update_data:
            return dict(existing)
        
        set_clause = ", ".join([f"{key} = ?" for key in update_data.keys()])
        values = list(update_data.values()) + [id]
        
        await db.execute(
            f"UPDATE todos SET {set_clause} WHERE id = ?",
            values
        )
        await db.commit()
        
        async with db.execute("SELECT * FROM todos WHERE id = ?", (id,)) as data:
            row = await data.fetchone()
            return dict(row)
    finally:
        await db.close()

@todo_router.delete("/{id}")
async def delete_todo(id: int):
    db = await get_db()
    try:
        async with db.execute("SELECT * FROM todos WHERE id = ?", (id,)) as data:
            existing = await data.fetchone()
            if not existing:
                raise HTTPException(status_code=404, detail="Todo not found")
        
        await db.execute("DELETE FROM todos WHERE id = ?", (id,))
        await db.commit()
        return {"Todo deleted successfully"}
    finally:
        await db.close()