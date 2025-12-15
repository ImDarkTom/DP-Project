import requests
import os

DATASET1_FILENAME="datasets/physical-activity.json"
DATASET2_FILENAME="datasets/walkability-index.csv"

def ensure_datasets_dir():
    # Ensure `datasets/` folder exists
    os.makedirs(os.path.dirname('./datasets/'), exist_ok=True)


# Dataset 1: Nutrition, Physical Activity, and Obesity
# Source: data.gov
# URL: https://catalog.data.gov/dataset/nutrition-physical-activity-and-obesity-behavioral-risk-factor-surveillance-system
def download_ds1():
    DATASET1_URL: str = "https://data.cdc.gov/api/views/hn4x-zwk7/rows.json"
    DATASET1_QUERY_PARAMS = { "accessType": "DOWNLOAD" }

    print("Starting download of dataset 1...")

    response = requests.get(DATASET1_URL, params=DATASET1_QUERY_PARAMS, stream=True)

    with open(DATASET1_FILENAME, mode="wb") as file:
        total_downloaded: int = 0

        for chunk in response.iter_content(chunk_size=10 * 1024):
            total_downloaded += len(chunk)
            print(f'Dataset 1 download: {total_downloaded/1024}KB')

            file.write(chunk)

    print("Finished downloading dataset 1")


# Dataset 2: Walkability Index 
# Source: data.gov
# URL: https://catalog.data.gov/dataset/walkability-index8
def download_ds2():
    DATASET2_URL = "https://edg.epa.gov/EPADataCommons/public/OA/EPA_SmartLocationDatabase_V3_Jan_2021_Final.csv"

    response = requests.get(DATASET2_URL, stream=True)

    print("Starting download of dataset 2...")

    with open(DATASET2_FILENAME, mode="wb") as file:
        total_downloaded: int = 0

        for chunk in response.iter_content(chunk_size=10 * 1024):
            total_downloaded += len(chunk)
            print(f'Dataset 2 download: {total_downloaded/1024}KB')

            file.write(chunk)

    print("Finished downloading dataset 2")

if __name__ == "__main__":
    ensure_datasets_dir()
    download_ds1()
    download_ds2()