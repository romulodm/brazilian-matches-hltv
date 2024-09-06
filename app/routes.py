from flask import render_template
import json
from app import app
from app.api.cron import cron_job

@app.route('/')
def index():
    try:
        with open('brazilian_matches.json') as f:
            matches = json.load(f)
    except FileNotFoundError:
        matches = []

    return render_template('index.html', matches=matches)

@app.route('/api/cron')
def index():
    cron_job()
