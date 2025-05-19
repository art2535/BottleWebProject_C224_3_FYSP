"""
Updated routes module to include the new sections.
"""

# routes.py
import os
import re
import json
from datetime import datetime
from bottle import route, view, request, redirect, response, template, static_file
from theory_algorithm import get_theory
from methods.graph_coloring_algorithm import greedy_graph_coloring, draw_colored_graph
from methods.bfs_spanning_tree import bfs_spanning_tree, draw_bfs_graph
from methods.dfs_spanning_tree import process_dfs_request
from logics.beam_utils import get_data
from logics.bfs_utils import get_bfs_data
import matplotlib.pyplot as plt
import matplotlib.colors

@route('/')
@route('/home')
@view('index')
def home():
    """Renders the home page."""
    return dict(year=datetime.now().year)

@route('/bfs', method=['GET', 'POST'])
@view('breadth_method')
def bfs():
    context = None
    context = get_bfs_data(request)
    context['year'] = datetime.now().year
    return context

@route('/dfs', method=['GET', 'POST'])
@view('depth_method')
def section2():
    """Renders section 2 with DFS spanning tree functionality."""
    data = process_dfs_request()
    data['year'] = datetime.now().year
    data['theory_text'] = get_theory('static/theory/dfs_theory.md')
    return data

@route('/beam', method=['GET', 'POST'])
@view('beam_method')
def beam():
    result = None
    result_is_error = False
    form_data, result, result_is_error = get_data(request)

    theory_text = get_theory('static/theory/theory_beam_search.md')

    return dict(
        year=datetime.now().year,
        result=result,
        result_is_error=result_is_error,
        form_data=form_data,
        theory_text=theory_text
    )


@route('/greedy_coloring', method=['GET', 'POST'])
@view('greedy_coloring_page')
def greedy_coloring_page():
    """Renders the graph coloring page and handles coloring logic."""
    year = datetime.now().year
    theory_text = get_theory('static/theory/graph_coloring_theory.md')

    # Initialize form_data with default or empty values to avoid None issues in template
    form_data = {'num_vertices': '3', 'adjacency_matrix': [[]]}  # Default to 3 for initial display
    # Initialize other variables to ensure they are always defined
    coloring_result_table_display = None
    graph_image_base64 = None
    num_colors_used_info = None
    error_message = None

    if request.method == 'POST':
        try:
            num_vertices_str = request.forms.get('num_vertices')
            if not num_vertices_str or not num_vertices_str.isdigit() or int(num_vertices_str) <= 0:
                raise ValueError("Number of vertices must be a positive integer.")

            num_vertices = int(num_vertices_str)
            form_data['num_vertices'] = num_vertices  # Store actual number used

            adjacency_matrix = []
            for i in range(num_vertices):
                row = []
                for j in range(num_vertices):
                    value_str = request.forms.get(f'edge_{i}_{j}')
                    if value_str is None:  # Handle case where input might be missing
                        raise ValueError(
                            f"Missing input for adjacency matrix at ({i},{j}). Ensure all cells are filled.")
                    if not value_str.isdigit() or int(value_str) not in [0, 1]:
                        raise ValueError(
                            f"Adjacency matrix values must be 0 or 1. Invalid value at ({i},{j}): '{value_str}'.")
                    value = int(value_str)
                    row.append(value)
                adjacency_matrix.append(row)
            form_data['adjacency_matrix'] = adjacency_matrix

            # Validate matrix symmetry and diagonal (optional, but good for coloring)
            for i in range(num_vertices):
                if adjacency_matrix[i][i] != 0:
                    error_message = f"Warning: Vertex {i} has a self-loop. Self-loops are typically ignored in simple graph coloring or imply the graph cannot be colored with 1 color at that vertex."
                    # Optionally, fix it: adjacency_matrix[i][i] = 0
                for j in range(i + 1, num_vertices):
                    if adjacency_matrix[i][j] != adjacency_matrix[j][i]:
                        # This should ideally be handled by "Make Symmetric" client-side
                        # or raise an error if strict undirected graph is expected.
                        # For now, we can choose to symmetrize it or warn.
                        # Symmetrizing by taking the 'OR' or 'MAX' of the two values:
                        # val = max(adjacency_matrix[i][j], adjacency_matrix[j][i])
                        # adjacency_matrix[i][j] = adjacency_matrix[j][i] = val
                        pass  # Assuming Welsh-Powell will handle it based on one side or symmetric input

            coloring_result, num_colors, _ = greedy_graph_coloring(adjacency_matrix)

            color_palette_for_table = []
            if num_colors > 0:
                # Ensure matplotlib is available here
                if num_colors <= 10:
                    cmap_table = plt.cm.get_cmap('tab10')
                    color_palette_for_table = [matplotlib.colors.to_hex(cmap_table(k)) for k in
                                               range(min(num_colors, 10))]
                elif num_colors <= 20:
                    cmap_table = plt.cm.get_cmap('tab20')
                    color_palette_for_table = [matplotlib.colors.to_hex(cmap_table(k)) for k in
                                               range(min(num_colors, 20))]
                else:
                    cmap_table = plt.cm.get_cmap('viridis')
                    # Sample num_colors from the continuous map
                    color_palette_for_table = [
                        matplotlib.colors.to_hex(cmap_table(k / (num_colors - 1 if num_colors > 1 else 1))) for k in
                        range(num_colors)]
                # If num_colors > len(color_palette_for_table) due to sampling limits, pad with a default or cycle
                while len(color_palette_for_table) < num_colors:
                    color_palette_for_table.append(
                        matplotlib.colors.to_hex(cmap_table((len(color_palette_for_table)) % cmap_table.N)))

            if coloring_result:
                sorted_coloring_items = sorted(coloring_result.items())
                coloring_result_table_display = []
                for vertex, color_id in sorted_coloring_items:
                    hex_color = "#808080"  # Default grey
                    if color_id > 0 and (color_id - 1) < len(color_palette_for_table):
                        hex_color = color_palette_for_table[color_id - 1]
                    elif color_id > 0:  # Fallback if palette is too small (should not happen with padding)
                        hex_color = color_palette_for_table[(color_id - 1) % len(color_palette_for_table)]
                    coloring_result_table_display.append(
                        {'vertex': vertex, 'color_id': color_id, 'hex_color': hex_color})

            num_colors_used_info = f"Number of colors used: {num_colors}"

            graph_image_base64 = draw_colored_graph(adjacency_matrix, coloring_result, num_colors)
            if graph_image_base64 is None and num_vertices > 0:
                error_message = (error_message + " " if error_message else "") + "Could not generate graph image."

        except ValueError as ve:
            error_message = str(ve)
            coloring_result_table_display = None
            graph_image_base64 = None
            num_colors_used_info = None
        except Exception as e:
            error_message = f"An unexpected server error occurred: {e}"
            coloring_result_table_display = None
            graph_image_base64 = None
            num_colors_used_info = None
            print(f"Error in greedy_coloring_page: {e}")  # Log to console for server-side debugging

    # For GET requests, or if POST failed and we need to repopulate the matrix size
    if request.method == 'GET' or error_message:
        if not form_data['adjacency_matrix'] or len(form_data['adjacency_matrix']) != int(
                form_data.get('num_vertices', 0)):
            # Initialize an empty matrix of the current num_vertices for the template to render
            try:
                current_num_v = int(form_data.get('num_vertices', 3))  # Default to 3 if not set
                if current_num_v > 0:
                    form_data['adjacency_matrix'] = [[0 for _ in range(current_num_v)] for _ in range(current_num_v)]
                else:
                    form_data['adjacency_matrix'] = [[]]
            except ValueError:
                form_data['num_vertices'] = '3'  # Reset to default on error
                form_data['adjacency_matrix'] = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    return dict(
        year=year,
        title='Greedy Graph Coloring',
        theory_text=theory_text,
        form_data=form_data,
        coloring_result_table=coloring_result_table_display,
        graph_image_base64=graph_image_base64,
        num_colors_used_info=num_colors_used_info,
        error_message=error_message
    )

@route('/our_team')
@view('our_team')
def our_command():
    members = [
        {
            'nickname': 'Meta4ora',
            'role': 'Back-end developer',
            'photo': '/static/dynamic/images/denis.jpg',
            'comment': 'He worked on the server logic and integration of bfs algorithm.'
        },
        {
            'nickname': 'art2535',
            'role': 'Back-end developer',
            'photo': '/static/dynamic/images/artem.jpg',
            'comment': 'Created a Beam Search algorithm and "Our team" visual style.'
        },
        {
            'nickname': 'Dyusha12',
            'role': 'Logics',
            'photo': '/static/dynamic/images/andrew.jpg',
            'comment': 'Developed algorithms for dfs and visual style for algorithm.'
        },
        {
            'nickname': 'setixx',
            'role': 'Designer',
            'photo': '/static/dynamic/images/maxim.jpg',
            'comment': 'Created the interface and visual style of the application.'
        }
    ]
    return dict(
        title="Our team",
        message="Our team",
        year=datetime.now().year,
        members=members
    )