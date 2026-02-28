import json
from pathlib import Path

DIR= Path('app/data')

user_path=DIR / 'users.json'
payment_path= DIR / 'payments.json'
session_path= DIR / 'session.json'
course_path= DIR / 'courses.json'

def read_json(file_path):
    try:
        with open(file_path, 'r') as f:
            data=json.load(f)
        
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    
def save_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)


