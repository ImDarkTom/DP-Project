# Data Programming Individual Project

Libraries:

- `requests` for downloading datasets.
- `pandas` for loading/analysing data.
- `sqlalchemy` for storing DataFrames using SQLite.
- `matplotlib` for visualising data insights.
- `tk` to enable interactive GUI for matplotlib.

## Downloading

1. Pull repo

```bash
git pull https://github.com/ImDarkTom/DP-Project.git
cd DP-Project/
```

2. Create venv and install dependencies.

```bash
python3 -m venv venv
source venv/bin/activate # Or on Windows, `venv\Scripts\activate`
pip install -r requirements.txt
```

## Running

### Option 1: Automatically Download, Process, & Visualise

1. Download datasets.

```bash
python3 main.py
```

### Option 2: Manually run scripts

1. Download datasets.

```bash
python3 src/download.py
```

2. Preprocess datasets and save to DB.

```bash
python3 src/processing.py
```


2. Visualise datasets info and save charts.

```bash
python3 src/visualisation.py
```

## Visualisations

Once ran, visualisations will be displayed both on-screen and saved to the directory `figures/`.