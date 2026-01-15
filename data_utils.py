import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_accidents_all_years(years=None):
    if years is None:
        years = [2020, 2021, 2022, 2023]

    frames = []
    for y in years:
        path = os.path.join(BASE_DIR, f'Data/{y}/caracteristiques-{y}.csv')
        if os.path.exists(path):
            frames.append(pd.read_csv(path, sep=';', low_memory=False))

    if not frames:
        return pd.DataFrame()

    return pd.concat(frames, ignore_index=True)


