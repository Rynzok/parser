import psycopg2
from psycopg2 import sql

# Параметры подключения
host = "localhost"  # или IP-адрес вашего сервера
database = "parser"
user = "user"
password = "user"


def open_db_connection():
    try:
        # Установка соединения
        connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )

        # Создание курсора для выполнения операций с базой данных
        cursor = connection.cursor()

        # Пример выполнения запроса
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print("Вы подключены к - ", db_version)

    except Exception as e:
        print("Ошибка при подключении к PostgreSQL", e)

    finally:
        # Закрытие курсора и соединения
        if cursor:
            cursor.close()
        if connection:
            connection.close()


open_db_connection()