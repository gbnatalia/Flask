'''
2. Создать API для получения списка фильмов по жанру. Приложение должно
иметь возможность получать список фильмов по заданному жанру.
Создайте модуль приложения и настройте сервер и маршрутизацию.
Создайте класс Movie с полями id, title, description и genre.
Создайте список movies для хранения фильмов.
Создайте маршрут для получения списка фильмов по жанру (метод GET).
Реализуйте валидацию данных запроса и ответа.

3.Создать API для добавления нового пользователя в базу данных. Приложение
должно иметь возможность принимать POST запросы с данными нового
пользователя и сохранять их в базу данных.
Создайте модуль приложения и настройте сервер и маршрутизацию.
Создайте класс User с полями id, name, email и password.
Создайте список users для хранения пользователей.
Создайте маршрут для добавления нового пользователя (метод POST).
Реализуйте валидацию данных запроса и ответа.

4. Создать API для обновления информации о пользователе в базе данных.
Приложение должно иметь возможность принимать PUT запросы с данными
пользователей и обновлять их в базе данных.
Создайте модуль приложения и настройте сервер и маршрутизацию.
Создайте класс User с полями id, name, email и password.
Создайте список users для хранения пользователей.
Создайте маршрут для обновления информации о пользователе (метод PUT).
Реализуйте валидацию данных запроса и ответа.

5. Создать API для удаления информации о пользователе из базы данных.
Приложение должно иметь возможность принимать DELETE запросы и
удалять информацию о пользователе из базы данных.
Создайте модуль приложения и настройте сервер и маршрутизацию.
Создайте класс User с полями id, name, email и password.
Создайте список users для хранения пользователей.
Создайте маршрут для удаления информации о пользователе (метод DELETE).
Реализуйте проверку наличия пользователя в списке и удаление его из
списка.
'''

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Movie(BaseModel):
    id: int
    title: str
    description: str
    genre: str

movies = []

@app.get("/movies", response_model=List[Movie])
async def get_movies():
    return movies

@app.post("/movies", response_model=Movie)
async def create_movie(movie: Movie):
    movie.id = len(movies) + 1
    users.append(movie)
    return movie


class User(BaseModel):
    id: int
    name: str
    email: str
    password: str

users = []

@app.get("/users", response_model=List[User])
async def get_users():
    return users

@app.post("/users", response_model=User)
async def create_user(user: User):
    user.id = len(users) + 1
    users.append(user)
    return user

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: User):
    for i in range(len(users)):
        if users[i].id == user_id:
            users[i] = user
            return user
    raise HTTPException(status_code=404,  default="User_not_found")

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    for i in range(len(users)):
        if users[i].id == user_id:
            del users[i]
            return {"message":"User deleted sucessfully"}
    raise HTTPException(status_code=404,  default="User_not_found")
