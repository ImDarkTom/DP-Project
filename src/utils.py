import os
import pandas as pd
import numpy as np

def ensure_dir(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def plot_correlation(x: pd.Series, y: pd.Series, ax, color: str):
    x.dropna(inplace=True)
    y.dropna(inplace=True)

    xv = x.values
    yv = y.values

    slope, intercept = np.polyfit(xv, yv, 1) # type: ignore
    line = slope * xv + intercept

    ax.plot(
        x, 
        line, 
        linestyle='-',
        color=color,
        alpha=0.5
    )