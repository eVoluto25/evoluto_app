
import csv
from datetime import datetime
import os

LOG_FILE = "system_logs.csv"

def init_log():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Event", "Status", "Details"])

def log_event(event, status, details=""):
    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().isoformat(), event, status, details])
