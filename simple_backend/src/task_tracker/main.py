from fastapi import FastAPI
from pathlib import Path
import json
from pydantic import BaseModel

app = FastAPI()


class TaskStorage:
    def __init__(self, file_path: str = "tasks.json"):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            self.file_path.write_text("[]")

    def read_tasks(self):
        with open(self.file_path, "r") as file:
            return json.load(file)

    def write_tasks(self, tasks):
        with open(self.file_path, "w") as file:
            json.dump(tasks, file, indent=4)

    def get_task(self, task_id):
        tasks = self.read_tasks()
        for task in tasks:
            if task["id"] == task_id:
                return task
        return None

    def add_task(self, task):
        tasks = self.read_tasks()
        tasks.append(task)
        self.write_tasks(tasks)

    def update_task(self, task_id, updated_task):
        tasks = self.read_tasks()
        for task in tasks:
            if task["id"] == task_id:
                task.update(updated_task)
                break
        self.write_tasks(tasks)

    def delete_task(self, task_id):
        tasks = self.read_tasks()
        tasks = [task for task in tasks if task["id"] != task_id]
        for i, task in enumerate(tasks):
            task["id"] = i + 1
        self.write_tasks(tasks)


storage = TaskStorage()

class Task(BaseModel):
    id: int
    title: str
    status: str

@app.get("/tasks")
def get_tasks():
    return storage.read_tasks()


@app.post("/tasks", response_model=Task)
def create_task(title: str, status: str = "ToDo"):
    task_id = len(storage.read_tasks()) + 1
    new_task = {"id": task_id, "title": title, "status": status}
    storage.add_task(new_task)
    return new_task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, title: str = None, status: str = None):
    task = storage.get_task(task_id)
    if not task:
        raise IndexError("Invalid id, task not found")
    if title:
        task["title"] = title
    if status:
        task["status"] = status
    storage.update_task(task_id, task)
    return task


@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int):
    try:
        task = storage.get_task(task_id)
        storage.delete_task(task_id)
        return f"Deleted task: {task}"
    except IndexError:
        return "Invalid id, task not found"
#
# print(create_task("Learning Python"))
# print(create_task("Learning GitHub"))
# print(create_task("Learning FastAPI"))
# print(create_task("Learning Django"))
# print(get_tasks())
# print(update_task(2, "Python & FastAPI", "Done"))
# print(update_task(1, None, "Done"))
#
# print(get_tasks())
# print(create_task("Learning Python"))
# print(create_task("Learning GitHub"))
# print(create_task("Learning FastAPI"))
# print(create_task("Learning Django"))
# print(delete_task(2))
# print(get_tasks())
