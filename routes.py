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

@route('/section4')
@view('section4')
def section4():
    """Renders section 4."""
    return dict(
        year=datetime.now().year
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