from flask import render_template
import json
import os
from app import app

@app.route('/')
def index():
    try:
        with open('brazilian_matches.json') as f:
            matches = json.load(f)
    except FileNotFoundError:
        matches = []

    return render_template('index.html', matches=matches)
