# Импорт стандартной библиотеки os
import os

# Импорт функции построения остовного дерева BFS и функции отрисовки графа
from methods.bfs_spanning_tree import bfs_spanning_tree, draw_bfs_graph

# Импорт функции получения теоретической информации
from theory_algorithm import get_theory

# Импорт объекта request из фреймворка Bottle
from bottle import request

# Функция для расчёта данных, связанных с алгоритмом обхода в ширину (BFS)
# Функция принимает аргумент `request`, содержащий HTTP-запрос
# Функция возвращает словарь с данными формы, результатами выполнения BFS, изображением графа и ошибками (если есть)
def get_bfs_data(request):
    # Получаем текст теории из markdown-файла
    theory_text = get_theory('static/theory/bfs_theory.md')

    # Инициализация значений формы по умолчанию
    form_data = {
        'num_vertices': '3',  # количество вершин по умолчанию
        'adjacency_matrix': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],  # пустая матрица смежности
        'start_vertex': '0'  # вершина начала обхода по умолчанию
    }

    # Переменные для хранения результатов
    result_matrix = None
    tree_vertices = None
    graph_image_path = '/static/dynamic/images/denis.jpg'  # путь к изображению графа по умолчанию
    error_message = None  # переменная для хранения сообщений об ошибке

    # Обработка POST-запроса (пользователь отправил форму)
    if request.method == 'POST':
        try:
            # Получаем количество вершин и проверяем корректность
            num_vertices_str = request.forms.get('num_vertices')
            if not num_vertices_str or not num_vertices_str.isdigit() or int(num_vertices_str) <= 0:
                raise ValueError("Number of vertices must be a positive integer.")
            num_vertices = int(num_vertices_str)
            form_data['num_vertices'] = num_vertices_str

            # Получаем стартовую вершину и проверяем корректность
            start_vertex_str = request.forms.get('start_vertex')
            if not start_vertex_str or not start_vertex_str.isdigit() or not (0 <= int(start_vertex_str) < num_vertices):
                raise ValueError(f"Start vertex must be in range [0, {num_vertices - 1}].")
            start_vertex = int(start_vertex_str)
            form_data['start_vertex'] = start_vertex_str

            # Считываем матрицу смежности из формы
            adjacency_matrix = []
            for i in range(num_vertices):
                row = []
                for j in range(num_vertices):
                    val = request.forms.get(f'edge_{i}_{j}')
                    if val is None:
                        raise ValueError(f"Missing value at ({i},{j})")
                    if val not in ['0', '1']:
                        raise ValueError(f"Invalid value at ({i},{j}) — must be 0 or 1")
                    row.append(int(val))
                adjacency_matrix.append(row)
            form_data['adjacency_matrix'] = adjacency_matrix

            # Проверка симметричности и отсутствия петель в матрице
            for i in range(num_vertices):
                if adjacency_matrix[i][i] != 0:
                    raise ValueError(f"Self-loop detected at vertex {i}")
                for j in range(i + 1, num_vertices):
                    if adjacency_matrix[i][j] != adjacency_matrix[j][i]:
                        raise ValueError(f"Matrix must be symmetric at ({i},{j})")

            # Выполнение BFS и построение остовного дерева
            result_matrix, tree_vertices = bfs_spanning_tree(num_vertices, adjacency_matrix, start_vertex)

            # Обработка возможной ошибки в виде строки
            if isinstance(result_matrix, str):
                error_message = result_matrix
                result_matrix = None
                tree_vertices = None
            else:
                # Отрисовка изображения графа на основе результата
                graph_image_path = draw_bfs_graph(result_matrix, adjacency_matrix, num_vertices)

        except Exception as e:
            # Обработка исключений и вывод сообщения об ошибке
            error_message = str(e)

    # При GET-запросе или при наличии ошибки — сбрасываем матрицу смежности
    if request.method == 'GET' or error_message:
        try:
            n = int(form_data.get('num_vertices', 3))
            form_data['adjacency_matrix'] = [[0 for _ in range(n)] for _ in range(n)]
        except:
            form_data['adjacency_matrix'] = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    # Возвращаем результат в виде словаря
    return {
        'form_data': form_data,  # исходные данные формы
        'result_matrix': result_matrix,  # результат BFS в виде матрицы
        'tree_vertices': tree_vertices,  # список вершин остовного дерева
        'graph_image_path': graph_image_path,  # путь к изображению графа
        'error_message': error_message,  # сообщение об ошибке, если есть
        'theory_text': theory_text  # текст теоретической части
    }
