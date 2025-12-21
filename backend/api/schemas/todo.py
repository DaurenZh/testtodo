from pydantic import BaseModel, Field
from typing import Optional

class TodoBase(BaseModel):
    task: str = Field(..., example="Buy groceries", max_length=255)
    done: bool = Field(default=False, example=False)

class TodoCreate(BaseModel):
    task: str = Field(..., example="Buy groceries", max_length=255)
    done: Optional[bool] = Field(default=False, example=False)

class TodoUpdate(BaseModel):
    task: Optional[str] = Field(None, max_length=255)
    done: Optional[bool] = Field(None, example=True)

class TodoResponse(BaseModel):
    id: int
    task: str
    done: bool

    class Config:
        from_attributes = True
