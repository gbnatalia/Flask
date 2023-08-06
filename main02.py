'''
Создать веб-приложение на FastAPI, которое будет предоставлять API для
работы с базой данных пользователей. Пользователь должен иметь
следующие поля:
    ○ ID (автоматически генерируется при создании пользователя)
    ○ Имя (строка, не менее 2 символов)
    ○ Фамилия (строка, не менее 2 символов)
    ○ Дата рождения (строка в формате "YYYY-MM-DD")
    ○ Email (строка, валидный email)
    ○ Адрес (строка, не менее 5 символов)
API должен поддерживать следующие операции:
    ○ Добавление пользователя в базу данных
    ○ Получение списка всех пользователей в базе данных
    ○ Получение пользователя по ID
    ○ Обновление пользователя по ID
    ○ Удаление пользователя по ID
Приложение должно использовать базу данных SQLite3 для хранения пользователей.
'''

from datetime import datetime, timedelta
from typing import List
from fastapi import FastAPI
from fastapi.params import Path
from pydantic import BaseModel, Field
import databases
import uvicorn
from sqlalchemy import Integer, String, DATE, Table, Column, create_engine, MetaData

DATABASE_URL = "sqlite:///home_database.db"
database = databases.Database(DATABASE_URL)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("first_name", String(50)),
    Column("last_name", String(50)),
    Column("birthday", String(50)),
    Column("email", String(50)),
    Column("address", String(150)),
)
metadata.create_all(engine)


class User(BaseModel):
    id: int = Field(default=None, alias='user_id')
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    birthday: str = Field(description='Дата в формате YYYY-MM-DD')
    email: str = Field(min_length=4, max_length=50)
    address: str = Field(min_length=5, max_length=150)


class UserInput(BaseModel):
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    birthday: str = Field(description='Дата в формате YYYY-MM-DD')
    email: str = Field(min_length=4, max_length=50)#regex=r'(\w+)[@]{1}(\w+)[.]{1}(\w+)')
    address: str = Field(min_length=5, max_length=150)


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get('/')
async def root():
    return {'message': 'Приветствие из задачи 2!'}


@app.get('/create_test_users/{count}')
async def create_test_users(count: int):
    for i in range(count):
         query = users.insert().values(
             first_name = f'FirstName{i}',
             last_name = f'LastName{i}',
             birthday = f'{datetime.strptime("2000-01-01", "%Y-%m-%d").date() + timedelta(days=i*10)}',
             email = f'Email_{i}@mail.ru',
             address = f'Address{i}'
            )
         await database.execute(query)
    return {'message': f'Создано {count} пользователей'}


@app.get('/users/', response_model=List[User])
async def get_all_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get('/users/{user_id}')
async def get_user(user_id: int = Path(..., title="id пользователя", ge=1)):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@app.post('/users/{user_id}', response_model=User)
async def add_user(user: UserInput):
    query = users.insert().values(
        first_name = user.first_name,
        last_name = user.last_name,
        birthday = datetime.strptime(user.birthday, '%Y-%m-%d').date(),
        email = user.email,
        address = user.address,
    )
    user_id = await database.execute(query)
    return  {'user_id': user_id} | dict(user)


@app.put('/users/{user_id}', response_model=User)
async def update_user(user_id: int, new_user: UserInput):
    query = users.update().where(users.c.id == user_id).values(dict(new_user))
    await database.execute(query)
    return {'user_id': user_id} | dict(new_user)


@app.delete('/users/{user_id}')
async def delete_user(user_id: int = Path(..., ge=1)):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': f'Пользователь с id = {user_id} удален!'}


if __name__ == '__main__':
    uvicorn.run("main02:app", host='127.0.0.1', port=8000, reload=True)