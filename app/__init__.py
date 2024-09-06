from flask import Flask
import threading
from app.job import run_schedule

app = Flask(__name__)

def start_scheduler():
    scheduler_thread = threading.Thread(target=run_schedule, daemon=True)
    scheduler_thread.start()

start_scheduler()

from app import routes