import matplotlib
import matplotlib.pyplot as plt

from src.lib.db import load_df_from_db
from src.utils import ensure_dir

from src.visualisations.vis1 import visualisation1
from src.visualisations.vis2 import visualisation2
from src.visualisations.vis3 import visualisation3
from src.visualisations.vis4 import visualisation4

# https://matplotlib.org/stable/gallery/color/named_colors.html

matplotlib.use('tkagg')

# https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html
plt.style.use("seaborn-v0_8")

def visualise_data():
    df = load_df_from_db()

    ensure_dir('./figures/')

    # Obesity and overweight change over time
    visualisation1(df)

    # weight class vs state avg walkability index
    visualisation2(df)

    # exercise vs walkability
    visualisation3(df)

    # diet vs weight class
    visualisation4(df)

    # todo: 
    # - diet vs income
    # - exercise vs weight class


if __name__ == "__main__":
    visualise_data()