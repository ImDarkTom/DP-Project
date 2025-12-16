import matplotlib
import matplotlib.pyplot as plt

from enums import Region, QuestionID, StratID
from utils import ensure_dir
from lib.db import load_df_from_db

df = load_df_from_db("physical_activity")

def filter_stats(
    region: Region,
    stratID: StratID,
    questionID: QuestionID,
):
    return df \
        .loc[df['LocationAbbr'] == region.value] \
        .loc[df['StratificationID1'] == stratID.value] \
        .loc[df['QuestionID'] == questionID.value] \
        .convert_dtypes()

def visualise_data():
    filtered = filter_stats(Region.ALL, StratID.OVERALL, QuestionID.OBESITY_18_PLUS)

    filtered.plot(x="Year", y="Data_Value", kind="line")

    plt.title("% of adults over 18 that have obesity")
    plt.xlabel("Year")
    plt.ylabel("% of population ")

    matplotlib.use('tkagg')

    # Save to file
    ensure_dir('./figures/')
    plt.savefig('./figures/figure1.png')

    plt.show()

if __name__ == "__main__":
    visualise_data()