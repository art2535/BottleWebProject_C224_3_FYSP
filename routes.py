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
from methods.bfs_spanning_tree import bfs_spanning_tree, draw_bfs_graph
from logics.greedy_utils import get_data as get_greedy_data
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
@view('greedy_coloring')
def greedy_coloring_page():
    year = datetime.now().year
    theory_text = get_theory('static/theory/graph_coloring_theory.md')

    form_data, coloring_result_table, graph_image_base64, num_colors_used_info, error_message = \
        get_greedy_data(request)

    return dict(
        year=year,
        title='Greedy Coloring',
        theory_text=theory_text,
        form_data=form_data,
        coloring_result_table=coloring_result_table,
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