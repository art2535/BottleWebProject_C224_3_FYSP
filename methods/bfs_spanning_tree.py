# bfs_algorithm.py
import os
import networkx as nx
import matplotlib.pyplot as plt

def bfs_spanning_tree(num_vertices, adjacency_matrix, start_vertex):
    """Implements BFS to build a spanning tree and returns the result matrix and vertices."""
    # Initialize result matrix and visited set
    result_matrix = [[0] * num_vertices for _ in range(num_vertices)]
    visited = [False] * num_vertices
    visited[start_vertex] = True
    queue = [start_vertex]
    tree_vertices = [start_vertex]
    edges = []

    # BFS traversal
    while queue:
        current = queue.pop(0)
        for neighbor in range(num_vertices):
            if adjacency_matrix[current][neighbor] == 1 and not visited[neighbor]:
                visited[neighbor] = True
                queue.append(neighbor)
                tree_vertices.append(neighbor)
                edges.append((current, neighbor))
                # Update result matrix (undirected graph, so set both directions)
                result_matrix[current][neighbor] = 1
                result_matrix[neighbor][current] = 1

    # Check if the graph is connected
    if len(tree_vertices) != num_vertices:
        return f"The spanning tree is not built: the graph is disconnected.", None

    return result_matrix, tree_vertices

def draw_bfs_graph(result_matrix, adjacency_matrix, num_vertices):
    """Draws the graph with the spanning tree highlighted and saves it."""
    G = nx.Graph()

    # Создаём вершины от 1 до num_vertices
    for i in range(1, num_vertices + 1):
        G.add_node(i)

    # Добавляем все рёбра из adjacency_matrix, сдвигая индексы на +1
    all_edges = []
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            if adjacency_matrix[i][j] == 1:
                all_edges.append((i + 1, j + 1))

    # Добавляем рёбра остовного дерева
    tree_edges = []
    if result_matrix:
        for i in range(num_vertices):
            for j in range(i + 1, num_vertices):
                if result_matrix[i][j] == 1:
                    tree_edges.append((i + 1, j + 1))

    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(6, 6))

    # Отрисовка всех рёбер
    nx.draw_networkx_edges(G, pos, edgelist=all_edges, edge_color='gray', width=1.5)

    # Отрисовка рёбер остовного дерева
    if result_matrix:
        nx.draw_networkx_edges(G, pos, edgelist=tree_edges, edge_color='red', width=2.5)

    # Отрисовка узлов и меток
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1000)
    labels = {i: str(i) for i in G.nodes}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=14)

    plt.title("Spanning Tree (red edges)")
    plt.tight_layout()
    static_path = 'static/dynamic/graphs/spanning_tree.png'
    os.makedirs(os.path.dirname(static_path), exist_ok=True)
    plt.savefig(static_path)
    plt.close()

    return f"/{static_path}"