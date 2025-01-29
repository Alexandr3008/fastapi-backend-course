from fastapi import FastAPI


app = FastAPI()

tasks = []


@app.get("/tasks")
def get_tasks():
    return tasks


@app.post("/tasks")
def create_task(name: str, status: str = "ToDo"):
    task_id = len(tasks) + 1
    new_task = {"id": task_id, "name": name, "status": status}
    tasks.append(new_task)
    return new_task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, new_name: str = None, new_status: str = None):
    for task in tasks:
        if task["id"] == task_id:
            if new_name is not None:
                task["name"] = new_name
            if new_status is not None:
                task["status"] = new_status
            return task
    raise FileNotFoundError("Invalid id, task not found")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    try:
        deleted_task = tasks.pop(task_id - 1)
        for i, task in enumerate(tasks):
            task["id"] = i + 1
        return {"Deleted task" : deleted_task}
    except IndexError:
        return "Invalid id, task not found"

print(create_task("Learning Python"))
print(create_task("Learning GitHub"))
print(create_task("Learning FastAPI"))
print(create_task("Learning Django"))
print(get_tasks())
print(update_task(2, "Python & FastAPI", "Done"))
print(update_task(1, None, "Done"))

print(get_tasks())
print(create_task("Learning Python"))
print(create_task("Learning GitHub"))
print(create_task("Learning FastAPI"))
print(create_task("Learning Django"))
print(delete_task(2))
print(get_tasks())