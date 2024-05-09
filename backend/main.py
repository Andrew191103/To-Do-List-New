from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import UUID, uuid4
from typing import List, Optional

app = FastAPI()

class TodoItem(BaseModel):
    id: UUID
    task: str
    status: str

class UpdateTodoItem(BaseModel):
    task: Optional[str]
    status: Optional[str]


todo_list = {
    UUID("2f5c7b81-8c1f-4db3-96a7-29e6db7a2aa6"): TodoItem(id=UUID("2f5c7b81-8c1f-4db3-96a7-29e6db7a2aa6"), task="Boxing", status="To Do"),
    UUID("8ffadce6-60d4-431f-afdb-3c53aac9d3c1"): TodoItem(id=UUID("8ffadce6-60d4-431f-afdb-3c53aac9d3c1"), task="Boxing", status="In Progress"),
    UUID("33d1f1c4-1ce4-46f5-9b88-dc42b86a0083"): TodoItem(id=UUID("33d1f1c4-1ce4-46f5-9b88-dc42b86a0083"), task="Roadwork", status="Done")
}

@app.get("/todo/get")
def get_todo_list():
    return {"TodoItems": list(todo_list.values())}

@app.get("/todo/get/{item_id}")
def get_todo_item(item_id: UUID):
    todo_item = todo_list.get(item_id)
    if not todo_item:
        raise HTTPException(status_code=404, detail="TodoItem not found")
    return {"TodoItem": todo_item}

@app.post("/todo/post")
def add_todo_item(todo_item: TodoItem):
    todo_list[todo_item.id] = todo_item
    return {"TodoItem": todo_item}

@app.delete("/todo/delete/{item_id}")
def delete_todo_item(item_id: UUID):
    if item_id in todo_list:
        del todo_list[item_id]
        return {"Success": True, "Message": "TodoItem deleted successfully"}
    else:
        return {"Success": False, "Message": "TodoItem not found"}

@app.put("/todo/put/{item_id}")
def update_todo_item(item_id: UUID, todo_data: UpdateTodoItem):
    if item_id not in todo_list:
        raise HTTPException(status_code=404, detail="TodoItem not found")
    if todo_data.task:
        todo_list[item_id].task = todo_data.task
    if todo_data.status:
        todo_list[item_id].status = todo_data.status
    return {"Success": True, "Message": "TodoItem updated successfully", "TodoItem": todo_list[item_id]}