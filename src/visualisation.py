import pandas
import matplotlib
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

from src.enums import *
from src.utils import ensure_dir

SQLITE_FILE_FILENAME="data.sqlite"

ENGINE = create_engine(f'sqlite:///{SQLITE_FILE_FILENAME}', echo=False)

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

df = pandas.read_sql_table(
    "physical_activity",
    con=ENGINE,
    index_col="index",
)

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