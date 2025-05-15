

"""
Updated routes module to include the new sections.
"""

import os
import re
import json
from datetime import datetime
from bottle import route, view, request, redirect, response, template, static_file

# Paths for data and logos
DATA_FILE = '/dynamic/logos/resultLogs.json'

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

@route('/section2')
@view('section2')
def section2():
    """Renders section 2."""
    return dict(
        year=datetime.now().year
    )

@route('/section3')
@view('section3')
def section3():
    """Renders section 3."""
    return dict(
        year=datetime.now().year
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