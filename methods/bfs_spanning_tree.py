import os
import networkx as nx
import matplotlib.pyplot as plt
"""
    Строит остовное дерево графа методом обхода в ширину (BFS).

    Входные параметры:
    - num_vertices (int): количество вершин в графе.
    - adjacency_matrix (List[List[int]]): матрица смежности графа.
    - start_vertex (int): индекс стартовой вершины (от 0 до num_vertices-1).

    Возвращает:
    - В случае связного графа:
        - result_matrix (List[List[int]]): матрица смежности остовного дерева.
        - tree_vertices (List[int]): список вершин остовного дерева.
        - edges (List[Tuple[int, int]]): список ребер остовного дерева.
    - Если граф несвязный:
        - строку с сообщением об ошибке,
        - None,
        - None.
    """
def bfs_spanning_tree(num_vertices, adjacency_matrix, start_vertex):
    # Инициализируем результирующую матрицу смежности для остовного дерева нулями
    result_matrix = [[0] * num_vertices for _ in range(num_vertices)]
    # Массив для отслеживания посещенных вершин
    visited = [False] * num_vertices
    # Отмечаем стартовую вершину как посещенную
    visited[start_vertex] = True
    # Очередь для BFS, начинаем со стартовой вершины
    queue = [start_vertex]
    # Список вершин, включенных в остовное дерево
    tree_vertices = [start_vertex]
    # Список ребер остовного дерева
    edges = []

    # Основной цикл обхода в ширину
    while queue:
        current = queue.pop(0)  # Извлекаем вершину из очереди
        # Перебираем всех соседей текущей вершины
        for neighbor in range(num_vertices):
            # Если сосед связан ребром и еще не посещен
            if adjacency_matrix[current][neighbor] == 1 and not visited[neighbor]:
                visited[neighbor] = True  # Отмечаем как посещенного
                queue.append(neighbor)    # Добавляем в очередь
                tree_vertices.append(neighbor)  # Добавляем в список вершин дерева
                edges.append((current, neighbor))  # Добавляем ребро в список
                # Обновляем результирующую матрицу смежности остовного дерева
                result_matrix[current][neighbor] = 1
                result_matrix[neighbor][current] = 1

    # Проверяем, что остовное дерево охватывает все вершины (граф связный)
    if len(tree_vertices) != num_vertices:
        return "The spanning tree is not built: the graph is disconnected.", None, None

    # Возвращаем матрицу остовного дерева, список вершин и ребер
    return result_matrix, tree_vertices, edges


def draw_bfs_graph(result_matrix, adjacency_matrix, num_vertices, bfs_edges=None):
    G = nx.Graph()  # Создаем пустой граф NetworkX
    # Добавляем вершины с номерами от 1 до num_vertices
    for i in range(1, num_vertices + 1):
        G.add_node(i)

    all_edges = []
    # Добавляем все ребра исходного графа (по верхнему треугольнику матрицы)
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            if adjacency_matrix[i][j] == 1:
                all_edges.append((i + 1, j + 1))

    tree_edges = []
    # Если переданы ребра остовного дерева, преобразуем их для визуализации
    if bfs_edges:
        # Сдвигаем индексы на +1, т.к. в NetworkX вершины нумеруются с 1
        tree_edges = [(u + 1, v + 1) for u, v in bfs_edges]

    # Генерируем координаты вершин для визуализации
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(6, 6))

    # Рисуем все ребра исходного графа серым цветом
    nx.draw_networkx_edges(G, pos, edgelist=all_edges, edge_color='gray', width=1.5)
    # Если есть ребра остовного дерева, рисуем их красным цветом поверх
    if tree_edges:
        nx.draw_networkx_edges(G, pos, edgelist=tree_edges, edge_color='red', width=2.5)

    # Рисуем вершины светло-голубого цвета
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1000)
    # Добавляем подписи к вершинам (номера вершин)
    labels = {i: str(i) for i in G.nodes}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=14)
    plt.title("Spanning Tree (red edges)")
    plt.tight_layout()

    # Создаем папки для сохранения файла, если их нет
    static_path = 'static/dynamic/graphs/spanning_tree.png'
    os.makedirs(os.path.dirname(static_path), exist_ok=True)
    # Сохраняем рисунок в файл
    plt.savefig(static_path)
    plt.close()

    # Возвращаем путь к сохраненному файлу (для использования, например, на вебе)
    return f"/{static_path}"
