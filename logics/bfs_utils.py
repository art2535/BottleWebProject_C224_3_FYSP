import os
from methods.bfs_spanning_tree import bfs_spanning_tree, draw_bfs_graph
from theory_algorithm import get_theory
from bottle import request
from logics.json_utils import save_algorithm_record

"""
    Что делает функция:
        Обрабатывает HTTP-запрос (GET или POST) от веб-формы для запуска алгоритма обхода графа

    Входные данные:
        request (bottle.Request): объект запроса, содержащий данные формы (метод, количество вершин,
                                  стартовую вершину, матрицу смежности).

    Выходные данные:
        dict: словарь со следующими ключами:
            - 'form_data' (dict): данные формы (кол-во вершин, матрица смежности, стартовая вершина),
            - 'result_matrix' (list[list[int]] | None): матрица остовного дерева, если построение прошло успешно,
            - 'tree_vertices' (list[int] | None): список вершин, входящих в остовное дерево,
            - 'graph_image_path' (str | None): путь к сгенерированному изображению графа,
            - 'error_message' (str | None): описание ошибки (если произошла),
            - 'theory_text' (str): HTML-контент с теорией по алгоритму BFS.
    """
def get_bfs_data(request):
    # Получаем текст теории из markdown-файла
    theory_text = get_theory('static/theory/bfs_theory.md')

    # Инициализация значений формы по умолчанию
    form_data = {
        'num_vertices': '3',
        'adjacency_matrix': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        'start_vertex': '0'
    }

    # Переменные для хранения результатов
    result_matrix = None
    tree_vertices = None
    graph_image_path = None
    error_message = None
    bfs_edges = None

    # Обработка POST-запроса (пользователь нажал "Build Graph")
    if request.method == 'POST':
        try:
            # Получаем количество вершин и проверяем корректность
            num_vertices_str = request.forms.get('num_vertices')
            if not num_vertices_str or not num_vertices_str.isdigit() or int(num_vertices_str) <= 0:
                raise ValueError("Number of vertices must be a positive integer.")
            num_vertices = int(num_vertices_str)
            form_data['num_vertices'] = num_vertices_str

            ## Получаем стартовую вершину и проверяем корректность
            start_vertex_str = request.forms.get('start_vertex')
            if not start_vertex_str or not start_vertex_str.isdigit() or not (1 <= int(start_vertex_str) <= num_vertices):
                raise ValueError(f"Start vertex must be in range [1, {num_vertices}].")
            start_vertex = int(start_vertex_str) - 1  # Перевод в 0-индексацию
            form_data['start_vertex'] = start_vertex_str  # Сохраняем исходное значение для формы


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
            result_matrix, tree_vertices, bfs_edges = bfs_spanning_tree(num_vertices, adjacency_matrix, start_vertex)

            # Обработка возможной ошибки в виде строки
            if isinstance(result_matrix, str):
                error_message = result_matrix
                result_matrix = None
                tree_vertices = None
                bfs_edges = None
            else:
                # Отрисовка изображения графа на основе результата
                graph_image_path = draw_bfs_graph(result_matrix, adjacency_matrix, num_vertices, bfs_edges)

        except Exception as e:
            # Обработка исключений и вывод сообщения об ошибке
            error_message = str(e)

        # Сохранение записи в JSON только после нажатия "Build Graph"
        save_algorithm_record('bfs', form_data, result_matrix, error_message)

    # При GET-запросе или при наличии ошибки — используем дефолтные значения
    if request.method == 'GET' or error_message:
        try:
            n = int(form_data.get('num_vertices', 3))
            if len(form_data['adjacency_matrix']) != n or any(len(row) != n for row in form_data['adjacency_matrix']):
                form_data['adjacency_matrix'] = [[0 for _ in range(n)] for _ in range(n)]
        except:
            form_data['adjacency_matrix'] = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    # Возвращаем результат в виде словаря
    return {
        'form_data': form_data,
        'result_matrix': result_matrix,
        'bfs_edges': [(u + 1, v + 1) for u, v in bfs_edges] if bfs_edges else None,
        'graph_image_path': graph_image_path,
        'error_message': error_message,
        'theory_text': theory_text
    }