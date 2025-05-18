# logics/bfs_util.py
import os
from methods.bfs_spanning_tree import bfs_spanning_tree, draw_bfs_graph
from theory_algorithm import get_theory
from bottle import request

def get_bfs_data(request):
    theory_text = get_theory('static/theory/bfs_theory.md')

    form_data = {
        'num_vertices': '3',
        'adjacency_matrix': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        'start_vertex': '0'
    }

    result_matrix = None
    tree_vertices = None
    graph_image_path = '/static/dynamic/images/denis.jpg'  # default image
    error_message = None

    if request.method == 'POST':
        try:
            num_vertices_str = request.forms.get('num_vertices')
            if not num_vertices_str or not num_vertices_str.isdigit() or int(num_vertices_str) <= 0:
                raise ValueError("Number of vertices must be a positive integer.")
            num_vertices = int(num_vertices_str)
            form_data['num_vertices'] = num_vertices_str

            start_vertex_str = request.forms.get('start_vertex')
            if not start_vertex_str or not start_vertex_str.isdigit() or not (0 <= int(start_vertex_str) < num_vertices):
                raise ValueError(f"Start vertex must be in range [0, {num_vertices - 1}].")
            start_vertex = int(start_vertex_str)
            form_data['start_vertex'] = start_vertex_str

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

            # Check for symmetry and no self-loops
            for i in range(num_vertices):
                if adjacency_matrix[i][i] != 0:
                    raise ValueError(f"Self-loop detected at vertex {i}")
                for j in range(i + 1, num_vertices):
                    if adjacency_matrix[i][j] != adjacency_matrix[j][i]:
                        raise ValueError(f"Matrix must be symmetric at ({i},{j})")

            # BFS traversal
            result_matrix, tree_vertices = bfs_spanning_tree(num_vertices, adjacency_matrix, start_vertex)

            if isinstance(result_matrix, str):  # error string
                error_message = result_matrix
                result_matrix = None
                tree_vertices = None
            else:
                graph_image_path = draw_bfs_graph(result_matrix, adjacency_matrix, num_vertices)

        except Exception as e:
            error_message = str(e)

    # Reinitialize matrix on GET or error
    if request.method == 'GET' or error_message:
        try:
            n = int(form_data.get('num_vertices', 3))
            form_data['adjacency_matrix'] = [[0 for _ in range(n)] for _ in range(n)]
        except:
            form_data['adjacency_matrix'] = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    return {
        'form_data': form_data,
        'result_matrix': result_matrix,
        'tree_vertices': tree_vertices,
        'graph_image_path': graph_image_path,
        'error_message': error_message,
        'theory_text': theory_text
    }
