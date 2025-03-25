import psycopg2
from psycopg2 import sql
from psycopg2 import extras

# Параметры подключения
host = "localhost"  # или IP-адрес вашего сервера
database = "parser"
user = "user"
password = "user"


def insert_first_list_in_db(insert_data):
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
        table_name = 'main'
        # Создание таблицы
        create_table_query = f'''
              CREATE TABLE IF NOT EXISTS {table_name} (
                  id SERIAL PRIMARY KEY,
                  key VARCHAR(100),
                  value TEXT
              );
              '''
        cursor.execute(create_table_query)
        print(f"Таблица {table_name} создана или уже существует.")


        # Формирование SQL-запроса для вставки нескольких строк
        insert_data_query = f'''
         INSERT INTO {table_name} (key, value) VALUES %s;
         '''

        # Используем psycopg2.extras для вставки нескольких строк

        extras.execute_values(cursor, insert_data_query, insert_data)

        print(f"Данные успешно вставлены в таблицу '{table_name}'.")

        connection.commit()

    except Exception as e:
        print("Ошибка при подключении к PostgreSQL", e)

    finally:
        # Закрытие курсора и соединения
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def insert_second_list_in_db(insert_data, table_name, reference_name):
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
        # Создание таблицы
        create_table_query = f'''
              CREATE TABLE IF NOT EXISTS {table_name} (
                  id SERIAL PRIMARY KEY,
                  key VARCHAR(100),
                  value TEXT
                  key_id INT REFERENCES {reference_name}(id)
              );
              '''
        cursor.execute(create_table_query)
        print(f"Таблица {table_name} создана или уже существует.")

        # Формирование SQL-запроса для вставки нескольких строк
        insert_data_query = f'''
         INSERT INTO {table_name} (key, value, key_id) VALUES %s;
         '''

        # Используем psycopg2.extras для вставки нескольких строк

        extras.execute_values(cursor, insert_data_query, insert_data)

        print(f"Данные успешно вставлены в таблицу '{table_name}'.")

        connection.commit()

    except Exception as e:
        print("Ошибка при подключении к PostgreSQL", e)

    finally:
        # Закрытие курсора и соединения
        if cursor:
            cursor.close()
        if connection:
            connection.close()



        # table_name_2 = 'company'
        # # Создание таблицы
        # create_table_query = f'''
        #       CREATE TABLE IF NOT EXISTS {table_name_2} (
        #           id SERIAL PRIMARY KEY,
        #           key_name VARCHAR(100),
        #           value VARCHAR(100),
        #           key_id INT REFERENCES {table_name}(id)
        #       );
        #       '''
        # cursor.execute(create_table_query)
        # print("Таблица 'company' создана или уже существует.")



        # # Вставка данных в таблицу
        # data_to_insert = [
        #     ('045', 'бери', 1),
        #     ('3765848', 'что хочешь', 1),
        #     ('23', 'но не меня', 1)
        # ]
        #
        # # Формирование SQL-запроса для вставки нескольких строк
        # insert_data_query = f'''
        #  INSERT INTO {table_name_2} (key_name, value, key_id) VALUES %s;
        #  '''
        #
        # # Используем psycopg2.extras для вставки нескольких строк
        #
        # extras.execute_values(cursor, insert_data_query, data_to_insert)
        #
        # print(f"Данные успешно вставлены в таблицу '{table_name_2}'.")
        #
        #
        # select_query = f'SELECT * FROM {table_name_2};'
        # cursor.execute(select_query)
        # rows = cursor.fetchall()
        # for row in rows:
        #     print(row)