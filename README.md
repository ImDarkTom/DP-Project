# Data Programming Individual Project

Libraries:

- `requests` for downloading datasets.
- `pandas` for loading/analysing data.
- `sqlalchemy` for storing DataFrames using SQLite.

## Running

1. Create venv and install dependencies.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Download datasets.

```bash
python3 download.py
```

3. Preprocess datasets and save to DB.

```bash
python3 loading.py
```
