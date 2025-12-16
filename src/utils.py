import os

def ensure_dir(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)