import sqlalchemy
from sqlalchemy import create_engine, MetaData
import plotly.graph_objects as go
import networkx as nx
from sqlalchemy.orm import sessionmaker

# Настройки подключения к базе данных
DATABASE_URI = 'postgresql+psycopg2://user:user@localhost:5556/parser'
# Создание подключения к базе данных
engine = create_engine(DATABASE_URI)
metadata = MetaData()
metadata.reflect(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

# Создание графа с помощью NetworkX
G = nx.Graph()
node_values = {}  # Словарь для хранения значений узлов

# Добавление таблиц и связей в граф
for table_name, table in metadata.tables.items():
    for fk in table.foreign_keys:
        parent_table_name = fk.column.table.name  # Имя родительской таблицы
        parent_column_name = 'id'  # Имя столбца в родительской таблице

        # Получение значения ключа из текущей таблицы
        first_row = session.query(table).first()  # Получаем первую строку
        if first_row is not None and hasattr(first_row, fk.column.name):
            child_key_value = getattr(first_row, fk.column.name)  # Значение внешнего ключа
            # Выполнение запроса к родительской таблице
            parent_row = session.query(fk.column.table).filter(getattr(fk.column.table.c, parent_column_name) == child_key_value).first()
            if parent_row is not None:
                node_values[table_name] = parent_row.value  # Сохраняем значение узла
                G.add_node(table_name)
            else:
                pass
        else:
            G.add_node(table_name)

    # Добавление связей (внешних ключей)
    for fk in table.foreign_keys:
        parent_table_name = fk.column.table.name
        G.add_edge(parent_table_name, table_name)  # Добавляем ребро между родительской и дочерней таблицей

# Получение координат узлов для визуализации
pos = nx.spring_layout(G)  # Используем алгоритм для расположения узлов

# Создание графика с помощью Plotly
edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)  # Разделитель между ребрами
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

# Создание графика
fig = go.Figure()

# Добавление ребер
fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode='lines', line=dict(width=0.5, color='#888'), hoverinfo='none'))

# Добавление узлов
node_x = []
node_y = []
node_text = []  # Список для текста узлов
node_hovertext = []
for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    # Добавляем значение узла для отображения при наведении
    node_text.append(f"{node}")
    node_hovertext.append(f"{node}: {node_values.get(node, 'N/A')}")

fig.add_trace(go.Scatter(
    x=node_x,
    y=node_y,
    mode='markers+text',
    text=node_text,
    textposition="top center",
    marker=dict(showscale=False, color='#6175c1', size=10, line_width=2),
    hoverinfo='text' , # Указываем, что хотим отображать текст при наведении
    hovertext=node_hovertext
))

# Настройка графика
fig.update_layout(showlegend=False, hovermode='closest', margin=dict(b=0, l=0, r=0, t=0), xaxis=dict(showgrid=False, zeroline=False, showticklabels=False), yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))

# Сохранение графика в HTML файл
fig.write_html("interactive_graph.html")

# Показать график
fig.show()
