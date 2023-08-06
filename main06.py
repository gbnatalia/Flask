'''
Необходимо создать базу данных для интернет-магазина. База данных должна
состоять из трех таблиц: товары, заказы и пользователи. Таблица товары должна
содержать информацию о доступных товарах, их описаниях и ценах. Таблица
пользователи должна содержать информацию о зарегистрированных
пользователях магазина. Таблица заказы должна содержать информацию о
заказах, сделанных пользователями.
    ○ Таблица пользователей должна содержать следующие поля: id (PRIMARY KEY),
    имя, фамилия, адрес электронной почты и пароль.
    ○ Таблица товаров должна содержать следующие поля: id (PRIMARY KEY),
    название, описание и цена.
    ○ Таблица заказов должна содержать следующие поля: id (PRIMARY KEY), id
    пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус
    заказа.
    Создайте модели pydantic для получения новых данных и возврата существующих в БД для каждой из трёх таблиц
(итого шесть моделей).
    Реализуйте CRUD операции для каждой из таблиц через создание маршрутов, REST API (итого 15 маршрутов).
    ○ Чтение всех
    ○ Чтение одного
    ○ Запись
    ○ Изменение
    ○ Удаление
'''

from datetime import datetime, timedelta, date
import random
from typing import List
from fastapi import FastAPI, Path
from pydantic import BaseModel, Field
import uvicorn
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DATE, ForeignKey
import databases

DATABASE_URL = "sqlite:///home_database3.db"
database = databases.Database(DATABASE_URL)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("first_name", String(50)),
    Column("last_name", String(50)),
    Column("email", String(50)),
    Column("password", String(150)),
)

products = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("description", String(150)),
    Column("price", Float)
)

orders = Table(
    "orders",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("goods_id", ForeignKey("goods.id"), nullable=False),
    Column("order_date", DATE),
    Column('status', String(20))
)

metadata.create_all(engine)


class User(BaseModel):
    id: int = Field(default=None)
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    email: str = Field(min_length=4, max_length=50)
    password: str = Field(min_length=5, max_length=150)


class UserInput(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    email: str = Field(..., min_length=4, max_length=50)
    password: str = Field(..., min_length=5, max_length=150)


class Product(BaseModel):
    id: int = Field(default=None)
    name: str = Field(min_length=2, max_length=50)
    description: str = Field(min_length=2, max_length=150)
    price: float = Field(..., ge=0.1, le=100000)


class ProductInput(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    description: str = Field(min_length=2, max_length=150)
    price: float = Field(..., ge=0.1, le=100000)


class Order(BaseModel):
    id: int = Field(default=None)
    order_date: date = Field(default=datetime.now())
    status: str = Field(default='in_progress')
    user_id: int
    goods_id: int


class OrderInput(BaseModel):
    order_date: date = Field(default=datetime.now())
    status: str = Field(default='in_progress')
    user_id: int
    goods_id: int


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get('/')
async def root():
    return {"message": "Online shop"}


@app.get('/create test_users/{count}')
async def create_test_users(count: int):
    for i in range(count):
        query = users.insert().values(first_name=f'user{i}', last_name=f'user{i}', email=f'email{i}@mail.ru',
                                      password=f'password{i}')
        await database.execute(query)
    return {'message': f'Создано {count} пользователей!'}


@app.get('/create test_products/{count}')
async def create_test_products(count: int):
    for i in range(count):
        query = products.insert().values( name=f'name{i}', description='description{i}',
                                          price=f'{random.randint(1, 100000):.2f}')
        await database.execute(query)
    return {'message': f'Создано {count} товаров!'}


@app.get('/create tes_orders/{count}')
async def create_test_orders(count: int):
    for i in range(count):
        query = orders.insert().values(
            order_date=datetime.strptime("2000-01-01", "%Y-%m-%d").date() + timedelta(days=i * 10),
            status=random.choice(['in_progress', 'done', 'cancelled']),
            user_id=random.randint(1, 10),
            goods_id=random.randint(1, 10)
        )
        await database.execute(query)
    return {'message': f'Создано {count} заказов'}


@app.get('/users/', response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get('/users/{user_id}', response_model=User)
async def read_user(user_id: int = Path(..., ge=1)):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@app.post('/users/', response_model=User)
async def create_user(user: UserInput):
    query = users.insert().values( first_name=user.first_name, last_name=user.last_name,
                                   email=user.email, password=user.password)
    user_id = await database.execute(query)
    return {'id': user_id} | dict(user)


@app.put('/users/{user_id}', response_model=User)
async def update_user(new_user: UserInput, user_id: int = Path(..., ge=1)):
    query = users.update().where(users.c.id == user_id).values(dict(new_user))
    await database.execute(query)
    return {'id': user_id} | dict(new_user)


@app.delete('/users/{user_id}')
async def delete_user(user_id: int = Path(..., ge=1)):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': f'Пользователь с id = {user_id} удален!'}


@app.get('/products/', response_model=List[Product])
async def get_all_products():
    query = products.select()
    return await database.fetch_all(query)


@app.get('/goods/{product_id}', response_model=Product)
async def get_product(product_id: int = Path(..., ge=1)):
    query = products.select().where(products.c.id == product_id)
    return await database.fetch_one(query)


@app.post('/products/', response_model=Product)
async def create_product(product: ProductInput):
    query = products.insert().values(name=product.name, description=product.description, price=product.price)
    actual_id = await database.execute(query)
    return {**product.dict(), 'id': actual_id}


@app.put('/products/{product_id}', response_model=Product)
async def update_product(new_product: ProductInput, product_id: int = Path(..., ge=1)):
    query = products.update().where(products.c.id == product_id).values(dict(new_product))
    await database.execute(query)
    return  {'id': product_id} | new_product


@app.delete('/products/{product_id}')
async def delete_product(product_id: int = Path(..., ge=1)):
    query = products.delete().where(products.c.id == product_id)
    await database.execute(query)
    return {'message': f'Товар с id = {product_id} удален!'}


@app.get('/orders/', response_model=List[Order])
async def get_all_orders():
    query = orders.select()
    return await database.fetch_all(query)


@app.get('/orders/{order_id}', response_model=Order)
async def get_order(order_id: int = Path(..., ge=1)):
    query = orders.select().where(orders.c.id == order_id)
    return await database.fetch_one(query)


@app.post('/orders/', response_model=Order)
async def create_order(order: OrderInput):
    query = orders.insert().values(
        order_date=order.order_date,
        status=order.status,
        user_id=order.user_id,
        goods_id=order.goods_id
        )
    actual_id = await database.execute(query)
    return {'id': actual_id} | dict(order)


@app.put('/orders/{order_id}', response_model=Order)
async def update_order(new_order: OrderInput, order_id: int = Path(..., ge=1)):
    query = orders.update().where(orders.c.id == order_id).values(**new_order.dict())
    await database.execute(query)
    return {'id': order_id} | dict(new_order)


@app.delete('/orders/{order_id}')
async def delete_order(order_id: int = Path(..., ge=1)):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {'message': f'Заказ с id = {order_id} удален!'}


if __name__ == '__main__':
    uvicorn.run('main06:app', host='127.0.0.1', port=8000, reload=True)
