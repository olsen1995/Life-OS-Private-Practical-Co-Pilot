from fastapi import FastAPI, Path, Header, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pydantic.v1 import SecretStr
import os
from typing import List, Optional

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/.well-known",
    StaticFiles(directory="static/well-known"),
    name="well-known",
)

@app.get("/.well-known/openapi.json")
async def serve_openapi():
    return FileResponse("static/well-known/openapi.json")

# In-memory data (for demo)
memory_store = []
task_store = []
task_id_counter = 1

# ----------------------------
# Models

class PromptRequest(BaseModel):
    prompt: str

class MemoryItem(BaseModel):
    text: str

class Task(BaseModel):
    id: Optional[int] = None
    title: str
    completed: Optional[bool] = False

# ----------------------------
# Auth Helper

def validate_api_key(x_api_key: str = Header(None)):
    expected_key = os.getenv("LIFEOS_API_KEY")
    if not expected_key or x_api_key != expected_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API key.")

# ----------------------------
# Routes

@app.post("/ask")
async def ask_question(request: PromptRequest, x_api_key: str = Header(None)):
    validate_api_key(x_api_key)

    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        return {"error": "Missing OPENAI_API_KEY"}

    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.7,
        api_key=SecretStr(openai_api_key),
    )

    prompt = ChatPromptTemplate.from_template("You are a helpful assistant. {input}")
    chain = prompt | llm
    result = chain.invoke({"input": request.prompt})

    return {"response": result.content}


@app.get("/memory")
def get_memory(x_api_key: str = Header(None)):
    validate_api_key(x_api_key)
    return {"memory": memory_store}


@app.post("/memory")
def add_memory(item: MemoryItem, x_api_key: str = Header(None)):
    validate_api_key(x_api_key)
    memory_store.append(item.text)
    return {"message": "Memory added successfully."}


@app.get("/tasks")
def get_tasks(x_api_key: str = Header(None)):
    validate_api_key(x_api_key)
    return {"tasks": task_store}


@app.post("/tasks")
def create_task(task: Task, x_api_key: str = Header(None)):
    validate_api_key(x_api_key)
    global task_id_counter
    task.id = task_id_counter
    task_id_counter += 1
    task_store.append(task.dict())
    return {"message": "Task created", "task": task}


@app.patch("/tasks/{task_id}")
def update_task(
    task_id: int = Path(...),
    updated_task: Task = Body(...),
    x_api_key: str = Header(None)
):
    validate_api_key(x_api_key)
    for task in task_store:
        if task["id"] == task_id:
            task.update(updated_task.dict(exclude_unset=True))
            return {"message": "Task updated", "task": task}
    return {"error": "Task not found"}


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int = Path(...), x_api_key: str = Header(None)):
    validate_api_key(x_api_key)
    global task_store
    task_store = [t for t in task_store if t["id"] != task_id]
    return {"message": f"Task {task_id} deleted."}
