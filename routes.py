"""
Updated routes module to include the new sections.
"""

import os
import re
import json
from datetime import datetime
from bottle import route, view, request, redirect, response, template, static_file
from theory_algorithm import get_theory
from beam_search_spanning_tree import beam_search_spanning_tree
from graph_coloring_algorithm import greedy_graph_coloring, draw_colored_graph

@route('/')
@route('/home')
@view('index')
def home():
    """Renders the home page."""
    return dict(year=datetime.now().year)

# Routes for sections 1-4
@route('/bfs')
@view('breadth_method')
def section1():
    """Renders section 1."""
    return dict(
        year=datetime.now().year
    )

@route('/dfs')
@view('depth_method')
def section2():
    """Renders section 2."""
    theory_text = get_theory('static/theory/dfs_theory.md')
    return dict(
        year=datetime.now().year,
        theory_text=theory_text
    )

@route('/beam', method=['GET', 'POST'])
@view('beam_method')
def beam():
    result = None
    result_is_error = False
    form_data = {'n': '', 'adjacency': [], 'weights': []}

    if request.method == 'POST':
        try:
            n = int(request.forms.get('n'))
            form_data['n'] = str(n)

            adjacency = []
            for i in range(n):
                row = []
                for j in range(n):
                    key = f'adjacency_{i}_{j}'
                    value = int(request.forms.get(key, 0))
                    row.append(value)
                adjacency.append(row)
            form_data['adjacency'] = adjacency
          
            weights = []
            for i in range(n):
                row = []
                for j in range(n):
                    key = f'weights_{i}_{j}'
                    value = int(request.forms.get(key, 0))
                    row.append(value)
                weights.append(row)
            form_data['weights'] = weights

            start = 0
            beam_width = 2

            tree_result = beam_search_spanning_tree(n, adjacency, weights, start, beam_width)
            result_is_error = isinstance(tree_result, str)
            result = tree_result

        except Exception as e:
            result = f"Error: {e}"
            result_is_error = True

    theory_text = get_theory('static/theory/theory_beam_search.md')

    return dict(
        year=datetime.now().year,
        result=result,
        result_is_error=result_is_error,
        form_data=form_data,
        theory_text=theory_text
    )


@route('/greedy_coloring', method=['GET', 'POST'])  # Changed route name
@view('greedy_coloring_page')  # Changed view name
def greedy_coloring_page():  # Changed function name
    """Renders the graph coloring page and handles coloring logic."""
    year = datetime.now().year
    theory_text = get_theory('static/theory/graph_coloring_theory.md')

    form_data = {'num_vertices': '', 'adjacency_matrix': []}
    coloring_result_table = None
    graph_image_path = None  # Will be base64 string
    num_colors_used_info = None
    error_message = None

    if request.method == 'POST':
        try:
            num_vertices_str = request.forms.get('num_vertices')
            if not num_vertices_str or not num_vertices_str.isdigit() or int(num_vertices_str) <= 0:
                raise ValueError("Number of vertices must be a positive integer.")

            num_vertices = int(num_vertices_str)
            form_data['num_vertices'] = num_vertices

            adjacency_matrix = []
            for i in range(num_vertices):
                row = []
                for j in range(num_vertices):
                    # Ensure matrix inputs are named like edge_i_j in the HTML
                    value = int(request.forms.get(f'edge_{i}_{j}', 0))
                    if value not in [0, 1]:
                        raise ValueError(f"Adjacency matrix values must be 0 or 1. Invalid value at ({i},{j}).")
                    row.append(value)
                adjacency_matrix.append(row)
            form_data['adjacency_matrix'] = adjacency_matrix

            # Ensure matrix is symmetric for undirected graph coloring
            for i in range(num_vertices):
                for j in range(i + 1, num_vertices):
                    if adjacency_matrix[i][j] != adjacency_matrix[j][i]:
                        # For simplicity, prefer the 1 if there's a mismatch, or handle as an error
                        # Here, we'll just proceed, but a real app might enforce symmetry or auto-correct.
                        # For now, we assume the "Make Symmetric" button handles this client-side if needed,
                        # or the algorithm handles it by considering the graph as undirected.
                        # The greedy algorithm typically expects an undirected graph representation.
                        pass

            coloring_result, num_colors, _ = greedy_graph_coloring(adjacency_matrix)

            # Prepare table for HTML display
            # Sort by vertex index for consistent display
            sorted_coloring_result = sorted(coloring_result.items())
            coloring_result_table = [{'vertex': item[0], 'color': item[1]} for item in sorted_coloring_result]

            num_colors_used_info = f"Number of colors used: {num_colors}"

            graph_image_path = draw_colored_graph(adjacency_matrix, coloring_result, num_colors)
            if graph_image_path is None and num_vertices > 0:
                error_message = "Could not generate graph image. Ensure vertices > 0."


        except ValueError as ve:
            error_message = str(ve)
            # Reset results if error
            coloring_result_table = None
            graph_image_path = None
            num_colors_used_info = None
        except Exception as e:
            error_message = f"An unexpected error occurred: {e}"
            coloring_result_table = None
            graph_image_path = None
            num_colors_used_info = None
            # Log the full error for debugging
            print(f"Error in greedy_coloring_page: {e}")

    return dict(
        year=year,
        title='Greedy Graph Coloring',
        theory_text=theory_text,
        form_data=form_data,
        coloring_result_table=coloring_result_table,
        graph_image_base64=graph_image_path,
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