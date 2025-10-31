import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent # project directory

def load_crop_data():
    data_path = BASE_DIR / "data" / "Soil_readings.csv"
    data = pd.read_csv(data_path)

    return data
