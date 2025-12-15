import requests;

# Dataset 1: Nutrition, Physical Activity, and Obesity
# Source: data.gov
# https://catalog.data.gov/dataset/nutrition-physical-activity-and-obesity-behavioral-risk-factor-surveillance-system

url: str = "https://data.cdc.gov/api/views/hn4x-zwk7/rows.json"
query_parameters = { "accessType": "DOWNLOAD" }

response = requests.get(url, params=query_parameters, stream=True)

with open("datasets/physical-activity.json", mode="wb") as file:
    total_downloaded: int = 0

    for chunk in response.iter_content(chunk_size=10 * 1024):
        total_downloaded += len(chunk)
        print(f'Downloaded: {total_downloaded/1024}KB')

        file.write(chunk)

print("Finished downloading dataset 1")


url: str = "https://data.cdc.gov/api/views/hn4x-zwk7/rows.json"
query_parameters = { "accessType": "DOWNLOAD" }

response = requests.get(url, params=query_parameters, stream=True)

with open("datasets/physical-activity.json", mode="wb") as file:
    total_downloaded: int = 0

    for chunk in response.iter_content(chunk_size=10 * 1024):
        total_downloaded += len(chunk)
        print(f'Downloaded: {total_downloaded/1024}KB')

        file.write(chunk)

print("Finished downloading dataset 1")