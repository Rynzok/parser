import sqlalchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.schema import Table
from graphviz import Digraph

# Настройки подключения к базе данных
DATABASE_URI = 'postgresql+psycopg2://user:user@localhost:5556/parser'

# Создание подключения к базе данных
engine = create_engine(DATABASE_URI)
metadata = MetaData()
metadata.reflect(bind=engine)

# Создание графа
dot = Digraph()

# Добавление таблиц в граф
for table_name, table in metadata.tables.items():
    dot.node(table_name, table_name)

    # Добавление связей (внешних ключей)
    for fk in table.foreign_keys:
        dot.edge(table_name, fk.column.table.name)

# Сохранение графа в файл
dot.render('database_structure', format='svg', cleanup=True)

print("Граф структуры базы данных сохранен как 'database_structure.png'")
