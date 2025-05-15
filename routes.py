

"""
Updated routes module to include the new sections.
"""

import os
import re
import json
from datetime import datetime
from bottle import route, view, request, redirect, response, template, static_file

# Paths for data and logos
UPLOAD_DIR = 'static/resources/logos'
DATA_FILE = 'static/resources/partners.json'
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Load data on startup
companies = []
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        companies = json.load(f)

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
