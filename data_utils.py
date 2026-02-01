import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Cache pour les données
_cache = {}


def load_accidents_data(year):
    """Charge les données d'accidents pour une année donnée."""
    cache_key = f'accidents_{year}'
    if cache_key in _cache:
        return _cache[cache_key]

    file_path = os.path.join(BASE_DIR, f'Data/{year}/caracteristiques-{year}.csv')
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, sep=';', low_memory=False)
        _cache[cache_key] = df
        return df
    return pd.DataFrame()


def load_accidents_all_years(years=None):
    """Charge les données d'accidents pour toutes les années."""
    if years is None:
        years = [2020, 2021, 2022, 2023]

    frames = []
    for y in years:
        df = load_accidents_data(y)
        if not df.empty:
            frames.append(df)

    if not frames:
        return pd.DataFrame()

    return pd.concat(frames, ignore_index=True)


def load_usagers_data(year):
    """Charge les données des usagers pour une année donnée."""
    cache_key = f'usagers_{year}'
    if cache_key in _cache:
        return _cache[cache_key]

    file_path = os.path.join(BASE_DIR, f'Data/{year}/usagers-{year}.csv')
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, sep=';', low_memory=False)
        _cache[cache_key] = df
        return df
    return pd.DataFrame()


def load_usagers_all_years(years=None):
    """Charge les données des usagers pour toutes les années."""
    if years is None:
        years = [2020, 2021, 2022, 2023]

    frames = []
    for y in years:
        df = load_usagers_data(y)
        if not df.empty:
            frames.append(df)

    if not frames:
        return pd.DataFrame()

    return pd.concat(frames, ignore_index=True)


def load_vehicules_data(year):
    """Charge les données des véhicules pour une année donnée."""
    cache_key = f'vehicules_{year}'
    if cache_key in _cache:
        return _cache[cache_key]

    file_path = os.path.join(BASE_DIR, f'Data/{year}/vehicules-{year}.csv')
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, sep=';', low_memory=False)
        _cache[cache_key] = df
        return df
    return pd.DataFrame()


def load_vehicules_all_years(years=None):
    """Charge les données des véhicules pour toutes les années."""
    if years is None:
        years = [2020, 2021, 2022, 2023]

    frames = []
    for y in years:
        df = load_vehicules_data(y)
        if not df.empty:
            frames.append(df)

    if not frames:
        return pd.DataFrame()

    return pd.concat(frames, ignore_index=True)


def load_lieux_data(year):
    """Charge les données des lieux pour une année donnée."""
    cache_key = f'lieux_{year}'
    if cache_key in _cache:
        return _cache[cache_key]

    file_path = os.path.join(BASE_DIR, f'Data/{year}/lieux-{year}.csv')
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, sep=';', low_memory=False)
        _cache[cache_key] = df
        return df
    return pd.DataFrame()


def load_complete_data(year=2023):
    """Charge et fusionne toutes les données pour une année."""
    cache_key = f'complete_{year}'
    if cache_key in _cache:
        return _cache[cache_key]

    accidents = load_accidents_data(year)
    usagers = load_usagers_data(year)
    vehicules = load_vehicules_data(year)
    lieux = load_lieux_data(year)

    if accidents.empty:
        return pd.DataFrame()

    data_complete = accidents.merge(usagers, on='Num_Acc', how='left')
    data_complete = data_complete.merge(vehicules, on=['Num_Acc', 'id_vehicule'], how='left', suffixes=('', '_veh'))
    data_complete = data_complete.merge(lieux, on='Num_Acc', how='left', suffixes=('', '_lieu'))

    _cache[cache_key] = data_complete
    return data_complete


def load_accidents_departement():
    """Charge les données d'accidents par département."""
    file_path = os.path.join(BASE_DIR, 'Data/2023/data-store/accidents_par_departement.csv')
    if os.path.exists(file_path):
        return pd.read_csv(file_path, sep=';', low_memory=False)
    return pd.DataFrame()


def load_accidents_population_ratio():
    """Charge les données du ratio accidents/population."""
    file_path = os.path.join(BASE_DIR, 'Data/2023/data-store/accidents_population_ratio.csv')
    if os.path.exists(file_path):
        return pd.read_csv(file_path, sep=';', low_memory=False)
    return pd.DataFrame()



