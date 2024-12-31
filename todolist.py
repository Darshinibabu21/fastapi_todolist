from fastapi import FastAPI , HTTPException
from typing import List
from pydantic import BaseModel

app=FastAPI()

class Todo(BaseModel):
    id:int
    title:str
    description:str=None
    status:str=None 
 
todos:List[Todo]=[]

@app.post("/todo",response_model=Todo)  #create todo
async def add(todo:Todo):
    if any(existing_todo.id == todo.id for existing_todo in todos):
        raise HTTPException(status_code=400 , detail="id already exists")
    todos.append(todo)
    return todo

@app.get("/todo",response_model=List[Todo])  #get all details
async def get_det():
    return todos

@app.get("/todo/{todo_id}",response_model=Todo)  #get particular id details
async def get_one(todo_id:int):
    for todo in todos:
        if todo.id==todo_id:
            return todo
    raise HTTPException(status_code=404,details="not found")

@app.put("/todo/{todo_id}",response_model=Todo)
async def update(todo_id:int , updated_todo:Todo):
    for index,todo in enumerate(todos):
        if todo_id==todo.id:
            todos[index]=updated_todo
            return updated_todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todo/{todo_id}")
async def dele(todo_id:int):
    global todos
    todos=[todo for todo in todos if todo.id!=todo_id]
    return {"message":"todo deleted successfully"}







