import heapq  # Модуль для работы с приоритетной очередью (кучей)
import os
import networkx as nx  # Библиотека для работы с графами
import matplotlib.pyplot as plt  # Библиотека для визуализации графиков

# Функция построения остовного дерева методом Beam Search
# Входные данные: количество вершин, матрица смежности, матрица весов ребер
# Возврат: граф матрицы, если успешно, иначе сообщение об ошибки
def beam_search_spanning_tree(n, adjacency_matrix, weight_matrix, start=0, beam_width=2):
    result_matrix = [[0] * n for _ in range(n)]  # Матрица результата (остовное дерево)
    visited = [False] * n  # Массив посещённых вершин
    visited[start] = True  # Начальная вершина помечается как посещённая

    edges = []  # Список всех рёбер с весами
    for i in range(n):
        for j in range(i + 1, n):
            if adjacency_matrix[i][j] and weight_matrix[i][j]:
                edges.append((weight_matrix[i][j], i, j))  # Добавляем ребро (вес, вершина1, вершина2)

    pq = [(0, [], {start})]  # Очередь состояний: (суммарный вес, рёбра, посещённые вершины)

    while pq:
        candidates = []  # Список лучших кандидатов на текущем уровне
        for _ in range(min(beam_width, len(pq))):  # Ограничиваем ширину луча
            if not pq:
                break
            total_weight, current_edges, current_visited = heapq.heappop(pq)  # Берём наименьший по весу путь
            candidates.append((total_weight, current_edges, current_visited))

        if not candidates:
            break

        for total_weight, current_edges, current_visited in candidates:
            for weight, u, v in sorted(edges):  # Перебираем рёбра по весу
                # Проверка на возможность добавить новое ребро без образования цикла
                if (u in current_visited and v not in current_visited) or (v in current_visited and u not in current_visited):
                    new_edges = current_edges + [(u, v, weight)]  # Обновляем список рёбер
                    new_visited = current_visited | {u, v}  # Обновляем посещённые вершины
                    new_total_weight = total_weight + weight  # Обновляем вес

                    # Условие окончания для небольших графов (n <= 4)
                    if n <= 4 and len(new_edges) == n - 2:
                        for u, v, _ in new_edges:
                            result_matrix[u][v] = result_matrix[v][u] = 1
                        draw_graph(result_matrix, adjacency_matrix, weight_matrix, n)
                        return result_matrix

                    # Условие окончания для графов >= 5 вершин
                    if n >= 5 and len(new_visited) == n:
                        for u, v, _ in new_edges:
                            result_matrix[u][v] = result_matrix[v][u] = 1
                        draw_graph(result_matrix, adjacency_matrix, weight_matrix, n)
                        return result_matrix

                    # Добавляем новое состояние в очередь
                    heapq.heappush(pq, (new_total_weight, new_edges, new_visited))

    # Если остовное дерево не построено (граф несвязный)
    draw_graph(None, adjacency_matrix, weight_matrix, n)
    return "The spanning tree is not built: the graph is disconnected."

# Функция для отображения графа и остовного дерева
# Вход: результирующая матрица смежности, входная матрица смежности, количество вершин
# Возврат: картинка графа
def draw_graph(result_matrix, adjacency_matrix, weight_matrix, n):
    G = nx.Graph()  # Создаём пустой граф

    for i in range(1, n + 1):
        G.add_node(i)  # Добавляем вершины (нумерация с 1)

    all_edges = []  # Все рёбра из матрицы смежности
    for i in range(n):
        for j in range(i + 1, n):
            if adjacency_matrix[i][j]:
                all_edges.append((i + 1, j + 1))  # Смещение индексов на 1

    tree_edges = []  # Рёбра остовного дерева (если есть)
    if result_matrix:
        for i in range(n):
            for j in range(i + 1, n):
                if result_matrix[i][j]:
                    tree_edges.append((i + 1, j + 1))

    pos = nx.spring_layout(G, seed=42)  # Расположение вершин на плоскости
    plt.figure(figsize=(6, 6))

    # Рисуем все рёбра серым цветом
    nx.draw_networkx_edges(G, pos, edgelist=all_edges, edge_color='gray', width=1.5)

    # Рисуем рёбра остовного дерева красным цветом
    if result_matrix:
        nx.draw_networkx_edges(G, pos, edgelist=tree_edges, edge_color='red', width=2.5)

    # Отображаем вершины и подписи
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1000)
    nx.draw_networkx_labels(G, pos, font_size=14)

    # Настройки и сохранение изображения
    plt.title("Spanning Tree (red edges)")
    plt.tight_layout()
    static_path = 'static/dynamic/graphs/spanning_tree.png'
    os.makedirs(os.path.dirname(static_path), exist_ok=True)
    plt.savefig(static_path)
    plt.close()