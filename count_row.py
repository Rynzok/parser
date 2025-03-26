import sqlalchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

# Настройки подключения к базе данных
DATABASE_URI = 'postgresql+psycopg2://user:user@localhost:5556/parser'

# Создание подключения к базе данных
engine = create_engine(DATABASE_URI)
metadata = MetaData()
metadata.reflect(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

# Получение всех таблиц
tables = metadata.tables.keys()

# Фильтрация таблиц по названию (5 цифр)
digit_tables = [table for table in tables if len(table) == 5 and table.isdigit()]

# Подсчет суммы строк для каждой таблицы
total_rows = 0
for table_name in digit_tables:
    table = metadata.tables[table_name]
    row_count = session.query(table).count()  # Подсчет строк в таблице
    total_rows += row_count
    print(f"Таблица: {table_name}, Количество строк: {row_count}")

print(f"Общее количество строк во всех таблицах: {total_rows}")

# Закрытие сессии
session.close()
