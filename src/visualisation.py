from src.lib.db import load_df_from_db
from src.utils import ensure_dir

from src.visualisations.vis1 import visualisation1
from src.visualisations.vis2 import visualisation2
from src.visualisations.vis3 import visualisation3
from src.visualisations.vis4 import visualisation4
from src.visualisations.vis5 import visualisation5
from src.visualisations.vis6 import visualisation6

from src.enums import Strat

# https://matplotlib.org/stable/gallery/color/named_colors.html

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

    # weight model
    visualisation5(df)
    visualisation5(df, Strat.AGE_18_TO_24, 'fig6_weight_class_model_age_18_24', 'Age 18-24', 'Population aged 18-24 (%)')
    visualisation5(df, Strat.AGE_45_TO_55, 'fig7_weight_class_model_age_45_55', 'Age 45-55', 'Population aged 45-55 (%)')

    # exercise vs weight class
    visualisation6(df)

    # todo: 
    # - diet vs income


if __name__ == "__main__":
    visualise_data()