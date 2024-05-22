import os

import pandas as pd
from peewee import Model, CharField, SqliteDatabase, DateField


# Создание БД с указанием пути
db_name = 'reviews.db'
path_to_db = os.path.join(os.getcwd(), 'database', db_name)
db = SqliteDatabase(path_to_db)


# Определение модели
class Review(Model):
    text = CharField()
    date = DateField()

    class Meta:
        database = db


# Функция для создания таблиц
def create_tables():
    with db:
        db.create_tables([Review])


# Функция для выгрузки всех данных из таблицы в DataFrame
def get_all_reviews() -> pd.DataFrame:
    query = Review.select()
    data = [{
        "text": review.text,
        "date": review.date
    } for review in query]
    return pd.DataFrame(data)


# Функция для вставки тестовых данных
def insert_test_data():
    data = [
        {"text": "Отличный коллектив и хорошая зарплата", "date": "2023.01.15"},
        {"text": "Плохой опыт, не рекомендую", "date": "2022.07.10"},
        {"text": "Средний сервис, но хорошая атмосфера", "date": "2023.03.05"},
        {"text": "Высокие зарплаты и приятное руководство", "date": "2021.11.20"},
        {"text": "Низкая зарплата, но отличный коллектив", "date": "2022.05.18"},
    ]

    with db.atomic():
        for review_data in data:
            Review.create(**review_data)
