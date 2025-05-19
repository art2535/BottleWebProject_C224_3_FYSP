# Импорт стандартного модуля для работы с путями файлов
import os

# Импорт библиотеки для работы с графами
import networkx as nx

# Импорт библиотеки для визуализации
import matplotlib.pyplot as plt

# Функция для построения остовного дерева с использованием обхода в ширину (BFS)
# Функция принимает:
#   - num_vertices: количество вершин в графе
#   - adjacency_matrix: матрицу смежности графа
#   - start_vertex: начальную вершину для BFS
# Функция возвращает:
#   - result_matrix: матрицу смежности остовного дерева
#   - tree_vertices: список посещённых вершин в порядке обхода
#   - В случае ошибки (если граф несвязный) — строку с сообщением об ошибке и None
def bfs_spanning_tree(num_vertices, adjacency_matrix, start_vertex):
    # Инициализируем результирующую матрицу остовного дерева нулями
    result_matrix = [[0] * num_vertices for _ in range(num_vertices)]

    # Массив для отслеживания посещённых вершин
    visited = [False] * num_vertices
    visited[start_vertex] = True

    # Очередь для обхода BFS
    queue = [start_vertex]

    # Список вершин в остовном дереве
    tree_vertices = [start_vertex]

    # Список рёбер остовного дерева (для построения графа, если нужно)
    edges = []

    # Основной цикл обхода в ширину
    while queue:
        current = queue.pop(0)  # извлекаем текущую вершину из очереди
        for neighbor in range(num_vertices):  # проходим по всем возможным соседям
            if adjacency_matrix[current][neighbor] == 1 and not visited[neighbor]:
                visited[neighbor] = True  # помечаем соседа как посещённого
                queue.append(neighbor)  # добавляем соседа в очередь
                tree_vertices.append(neighbor)  # добавляем в список дерева
                edges.append((current, neighbor))  # добавляем ребро

                # Обновляем результатирующую матрицу (граф неориентированный)
                result_matrix[current][neighbor] = 1
                result_matrix[neighbor][current] = 1

    # Проверка: если не все вершины посещены — граф несвязный
    if len(tree_vertices) != num_vertices:
        return f"The spanning tree is not built: the graph is disconnected.", None

    return result_matrix, tree_vertices


# Функция для отрисовки графа с выделением остовного дерева
# Функция принимает:
#   - result_matrix: матрицу смежности остовного дерева (если None — рисуется только исходный граф)
#   - adjacency_matrix: исходная матрица смежности
#   - num_vertices: количество вершин
# Функция возвращает:
#   - путь к сохранённому изображению графа в формате PNG
def draw_bfs_graph(result_matrix, adjacency_matrix, num_vertices):
    G = nx.Graph()  # создаём пустой граф

    # Добавляем вершины с номерами от 1 до num_vertices
    for i in range(1, num_vertices + 1):
        G.add_node(i)

    # Добавляем все рёбра из матрицы смежности (с индексами +1, для красивого отображения)
    all_edges = []
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            if adjacency_matrix[i][j] == 1:
                all_edges.append((i + 1, j + 1))

    # Добавляем рёбра, входящие в остовное дерево (если оно есть)
    tree_edges = []
    if result_matrix:
        for i in range(num_vertices):
            for j in range(i + 1, num_vertices):
                if result_matrix[i][j] == 1:
                    tree_edges.append((i + 1, j + 1))

    # Располагаем вершины графа на плоскости
    pos = nx.spring_layout(G, seed=42)

    # Создаём фигуру для графика
    plt.figure(figsize=(6, 6))

    # Отрисовываем все рёбра серым цветом
    nx.draw_networkx_edges(G, pos, edgelist=all_edges, edge_color='gray', width=1.5)

    # Отрисовываем рёбра остовного дерева красным цветом
    if result_matrix:
        nx.draw_networkx_edges(G, pos, edgelist=tree_edges, edge_color='red', width=2.5)

    # Отрисовываем вершины и их подписи
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1000)
    labels = {i: str(i) for i in G.nodes}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=14)

    # Устанавливаем заголовок графика
    plt.title("Spanning Tree (red edges)")

    # Компактно располагаем элементы
    plt.tight_layout()

    # Указываем путь для сохранения изображения
    static_path = 'static/dynamic/graphs/spanning_tree.png'

    # Создаём директорию, если она ещё не существует
    os.makedirs(os.path.dirname(static_path), exist_ok=True)

    # Сохраняем изображение и закрываем график
    plt.savefig(static_path)
    plt.close()

    # Возвращаем относительный путь к изображению
    return f"/{static_path}"