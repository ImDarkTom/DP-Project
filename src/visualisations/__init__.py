import matplotlib.pyplot as plt

from src.lib.db import load_df_from_db

# https://realpython.com/python-init-py/

# Whenever we run a file within this folder/module, we automatically apply this style
plt.style.use("seaborn-v0_8")

# Load the dataframe once for all visualisations to use
df = load_df_from_db()