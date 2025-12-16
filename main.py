from src.download import download_datasets
from src.processing import process_datasets
from src.visualisation import visualise_data

if __name__ == "__main__":
    download_datasets()
    process_datasets()
    visualise_data()
    