import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from bottle import request
import random
import os
import json

from logics.json_utils import save_algorithm_record

def create_spanning_tree(adj_matrix, start_vertex):
    """Create a spanning tree using DFS from the adjacency matrix."""
    n = len(adj_matrix)
    G_full = nx.Graph()

    # Добавляем все вершины
    G_full.add_nodes_from(range(n))

    # Добавляем рёбра, пропуская петли (i == j)
    for i in range(n):
        for j in range(i + 1, n):
            if adj_matrix[i][j] == 1:
                G_full.add_edge(i, j)

    start_vertex = start_vertex - 1  # Индексация с 0

    try:
        dfs_edges = list(nx.dfs_edges(G_full, source=start_vertex))
        T_tree = nx.Graph()
        T_tree.add_nodes_from(range(n))
        T_tree.add_edges_from(dfs_edges)

        tree_matrix = nx.to_numpy_array(T_tree, dtype=int).tolist()
        vertices_list = list(range(1, n + 1))
        return G_full, T_tree, tree_matrix, vertices_list, None
    except nx.NetworkXError as e:
        return None, None, None, None, str(e)




def generate_random_matrix(n):
    """Generate a random adjacency matrix for a connected graph."""
    matrix = [[0] * n for _ in range(n)]
    vertices = list(range(n))
    random.shuffle(vertices)
    for i in range(n - 1):
        u, v = vertices[i], vertices[i + 1]
        matrix[u][v] = matrix[v][u] = 1

    # Add some random edges
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < 0.3 and matrix[i][j] == 0:
                matrix[i][j] = matrix[j][i] = 1
    return matrix


def save_to_json(adj_matrix, start_vertex, tree_matrix, filename="static/dynamic/graphs/dfs_data.json"):
    """Save input and output data to a JSON file."""
    data = {
        "dfs": {
            "adjacency_matrix": adj_matrix,
            "start_vertex": start_vertex,
            "tree_matrix": tree_matrix
        }
    }
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def save_graph_image(G_full, T_tree, filename="static/dynamic/graphs/spanning_tree_dfs_1.png"):
    """Save graph to a PNG file with red edges for the spanning tree."""
    plt.figure(figsize=(6, 6))
    
    # Получаем позицию для узлов
    pos = nx.spring_layout(G_full, seed=42)  

    # Рисуем граф с серыми рёбрами
    nx.draw_networkx_edges(G_full, pos, edge_color='lightgray', width=1)

    # Рисуем красные рёбра для дерева
    nx.draw_networkx_edges(T_tree, pos, edgelist=T_tree.edges(), edge_color='red', width=2)

    # Рисуем узлы
    nx.draw_networkx_nodes(G_full, pos, node_color='lightblue', node_size=500)

    # Отображаем метки вершин с сдвигом на 1 (для отображения вершин с 1, а не с 0)
    labels = {node: node + 1 for node in G_full.nodes}  # Сдвигаем индексы на 1
    nx.draw_networkx_labels(G_full, pos, labels=labels, font_size=12, font_weight='bold')

    # Сохраняем изображение
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(filename, format='png')
    plt.close()

    return filename


def save_to_json(adj_matrix, start_vertex, tree_matrix, filename="static/dynamic/graphs/dfs_data.json"):
    """Save input and output data to a JSON file."""
    data = {
        "dfs": {
            "adjacency_matrix": adj_matrix,
            "start_vertex": start_vertex,
            "tree_matrix": tree_matrix
        }
    }
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def validate_input(vertices, start_vertex, adj_matrix):
    """Validate user input."""
    if not isinstance(vertices, int) or not (1 <= vertices <= 8):
        return "Number of vertices must be an integer between 1 and 8"
    if not isinstance(start_vertex, int) or not (1 <= start_vertex <= vertices):
        return "Starting vertex must be an integer between 1 and number of vertices"
    if not adj_matrix or len(adj_matrix) != vertices or any(len(row) != vertices for row in adj_matrix):
        return "Invalid adjacency matrix dimensions"
    for i in range(vertices):
        for j in range(vertices):
            if not isinstance(adj_matrix[i][j], int) or adj_matrix[i][j] not in [0, 1]:
                return "Matrix elements must be integers 0 or 1"
    return None

def process_dfs_request():
    """Process DFS spanning tree request and return data."""
    error = None
    graph_path = None
    tree_matrix = None
    vertices_list = None
    adj_matrix = None
    vertices = 3  # Default
    start_vertex = 1  # Default start vertex set to 1 (from 1-based index)
    
    if request.method == 'POST':
        try:
            action = request.forms.get('action')
            vertices = request.forms.get('vertices', '3')
            vertices = int(vertices) if vertices.strip() else 3
            
            if action == 'generate':
                # Generate random matrix
                adj_matrix = generate_random_matrix(vertices)
                start_vertex = random.randint(1, vertices)  # Adjusted to 1-based index
            else:
                # Get matrix from form
                adj_matrix = []
                for i in range(vertices):
                    row = []
                    for j in range(vertices):
                        val = request.forms.get(f'edge_{i+1}_{j+1}', '0').strip()  # Adjust to 1-based index
                        row.append(int(val) if val else 0)
                    adj_matrix.append(row)

                start_vertex = request.forms.get('start_vertex', '1').strip()  # Adjust to 1-based index
                start_vertex = int(start_vertex) if start_vertex else 1
            
            # Validate input
            error = validate_input(vertices, start_vertex, adj_matrix)
            
            if not error and action == 'build':
                # Create spanning tree
                G, T, tree_matrix, vertices_list, graph_error = create_spanning_tree(adj_matrix, start_vertex)

                if graph_error:
                    error = graph_error
                elif G and T:
                    graph_path = save_graph_image(G, T)
                    save_to_json(adj_matrix, start_vertex, tree_matrix)

                # Логирование независимо от результата (с ошибкой или нет)
                input_data = {
                    'num_vertices': vertices,
                    'adjacency_matrix': adj_matrix,
                    'start_vertex': start_vertex
                }
                save_algorithm_record(
                    algorithm='dfs',
                    input_data=input_data,
                    result_matrix=tree_matrix if tree_matrix else None,
                    error_message=error
                )


        except (ValueError, TypeError) as e:
            error = "Invalid input: Please enter valid numbers"
            print(e)
    
    # Prepare matrix for template
    if not adj_matrix:
        adj_matrix = [[0] * vertices for _ in range(vertices)]
    
    return {
        'vertices': vertices,
        'adj_matrix': adj_matrix,
        'start_vertex': start_vertex,
        'graph_path': graph_path,
        'tree_matrix': tree_matrix,
        'vertices_list': vertices_list,
        'error': error
    }

