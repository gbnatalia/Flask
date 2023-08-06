'''
Напишите API для управления списком задач. Для этого создайте модель Task
со следующими полями:
    ○ id: int (первичный ключ)
    ○ title: str (название задачи)
    ○ description: str (описание задачи)
    ○ done: bool (статус выполнения задачи)
API должно поддерживать следующие операции:
    ○ Получение списка всех задач: GET /tasks/
    ○ Получение информации о конкретной задаче: GET /tasks/{task_id}/
    ○ Создание новой задачи: POST /tasks/
    ○ Обновление информации о задаче: PUT /tasks/{task_id}/
    ○ Удаление задачи: DELETE /tasks/{task_id}/
Для валидации данных используйте параметры Field модели Task.
Для работы с базой данных используйте SQLAlchemy и модуль databases.
'''
from fastapi import FastAPI, Path
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean
from typing import List
import uvicorn
import databases
import random

DATABASE_URL = "sqlite:///home_database2.db"
database = databases.Database(DATABASE_URL)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = MetaData()

tasks = Table(
    "tasks",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(50)),
    Column('description', String(150)),
    Column('done', Boolean),
)

metadata.create_all(engine)

class Task(BaseModel):
    id: int = Field(default=None)
    title: str = Field(max_length=50)
    description: str = Field(default=None, max_length=150)
    done: bool = Field(default=False)


class TaskInput(BaseModel):
    title: str = Field(max_length=50)
    description: str = Field(default=None, max_length=150)
    done: bool = Field(default=False)


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get('/')
async def root():
    return {"message": "Приветствие из задачи 4!"}


@app.get('/create_test tasks/{count}')
async def create_test_tasks(count: int = Path(..., ge=1)):
    for i in range(count):
        query = tasks.insert().values( title=f'task{i}',description=f'description {i}',done=random.choice([True, False]))
        await database.execute(query)
    return {'message': f'Создано {count} задач!'}


@app.get('/tasks/', response_model=List[Task])
async def get_all_tasks():
    query = tasks.select()
    return await database.fetch_all(query)


@app.get('/tasks/{task_id}/', response_model=Task)
async def get_task(task_id: int = Path(..., ge=1, le=15)):
    query = tasks.select().where(tasks.c.id == task_id)
    return await database.fetch_one(query)


@app.post('/tasks/', response_model=Task)
async def create_task(task: TaskInput):
    query = tasks.insert().values( title=task.title, description=task.description, done=task.done)
    task_id = await database.execute(query)
    return {'id': task_id} | dict(task)


@app.put('/tasks/{task_id}/', response_model=Task)
async def edit_task(new_task: TaskInput, task_id: int = Path(..., ge=1)):
    query = tasks.update().where(tasks.c.id == task_id).values(dict(new_task))
    await database.execute(query)
    return {'id': task_id} | dict(new_task)


@app.delete('/tasks/{task_id}/')
async def delete_task(task_id: int = Path(..., ge=1)):
    query = tasks.delete().where(tasks.c.id == task_id)
    await database.execute(query)
    return {'message': f'Задача с id = {task_id} удалена!'}


if __name__ == '__main__':
    uvicorn.run('main4:app', host='127.0.0.1', port=8000, reload=True)
