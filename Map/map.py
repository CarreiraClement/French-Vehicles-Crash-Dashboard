import folium
import pandas
import json
import numpy as np
from branca.colormap import linear
import copy

import os

from data_utils import load_accidents_all_years

coords = (43.25089, 2.43844)
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
geo_json_data = os.path.join(base_dir, 'Data/geojson/departements.geojson')

tiles = "https://{s}.tile.jawg.io/jawg-light/{z}/{x}/{y}{r}.png?access-token=WxkdBMM2vf10JFvs7ISABaUnFIMB1eszkdkVnEGeLYiViNpEJsFOakojFkygRWeJ"
attr = '&copy; <a href="https://www.jawg.io">Jawg</a> &amp; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'


def generate_map_accidents_html(year=None):
    """
    Génère la carte du nombre d'accidents par département
    """
    if year is None or year == "total":
        accidents_data = load_accidents_all_years()
    else:
        accidents_data = pandas.read_csv(
            os.path.join(base_dir, f'Data/{year}/caracteristiques-{year}.csv'),
            sep=';'
        )

    if accidents_data.empty:
        map_obj = folium.Map(
            location=coords,
            tiles=tiles,
            attr=attr,
            zoom_start=6
        )
        return map_obj._repr_html_()

    accident_by_department = accidents_data.groupby('dep').size().reset_index(name='nb_accidents')

    with open(geo_json_data, 'r', encoding='utf-8') as f:
        geojson = json.load(f)

    accidents_dict = dict(zip(accident_by_department['dep'].astype(str), accident_by_department['nb_accidents']))

    accident_by_department['nb_accidents_log'] = np.log1p(accident_by_department['nb_accidents'])

    map_obj = folium.Map(
        location=coords,
        tiles=JAWG_TILES,
        attr=JAWG_ATTR,
        zoom_start=5.4
    )

    folium.Choropleth(
        geo_data=geo_json_data,
        data=accident_by_department,
        columns=["dep", "nb_accidents_log"],
        key_on="feature.properties.code",
        fill_color='YlOrBr',
        fill_opacity=0.85,
        legend_name="Nombre d'accidents par département",
        line_weight=1.5,
        bins=8
    ).add_to(map_obj)

    for feature in geojson['features']:
        code = feature['properties']['code']
        feature['properties']['nb_accidents'] = accidents_dict.get(str(code), 0)

    folium.GeoJson(
        geojson,
        style_function=lambda feature: {
            'fillColor': 'transparent',
            'fillOpacity': 0,
            'weight': 0,
            'color': 'transparent'
        },
        highlight_function=lambda feature: {
            'fillColor': '#922d50',
            'fillOpacity': 0.6,
            'weight': 2,
            'color': '#3c1b43'
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['nom', 'code', 'nb_accidents'],
            aliases=['Département: ', 'Code: ', "Nombre d'accidents: "],
            localize=True
        ),
        overlay=True,
        control=False
    ).add_to(map_obj)

    return map_obj._repr_html_()


def generate_map_ratio_html(year=None):
    """
    Génère la carte du ratio accidents/population par département.
    """
    if year is None or str(year).lower() == "total":
        accidents_data = load_accidents_all_years()
    else:
        accidents_data = pandas.read_csv(
            os.path.join(base_dir, f'Data/{year}/caracteristiques-{year}.csv'),
            sep=';'
        )

    if accidents_data.empty:
        map_accidents_ratio = folium.Map(
            location=coords,
            tiles=JAWG_TILES,
            attr=JAWG_ATTR,
            zoom_start=5.4
        )
        return map_accidents_ratio._repr_html_()

    accident_by_department = accidents_data.groupby('dep').size().reset_index(name='nb_accidents')

    population_data = pandas.read_csv(
        os.path.join(base_dir, 'Data/population/donnees_departements.csv'),
        sep=';'
    )

    population_by_dep = population_data[['DEP', 'PTOT']].copy()
    population_by_dep.columns = ['dep', 'population']

    population_by_dep['dep'] = population_by_dep['dep'].astype(str)
    accident_by_department['dep'] = accident_by_department['dep'].astype(str)

    accidents_population = accident_by_department.merge(
        population_by_dep,
        on='dep',
        how='left'
    )

    accidents_population['ratio_accidents_pop'] = (
        accidents_population['nb_accidents'] / accidents_population['population'] * 1000
    ).fillna(0)

    accidents_population['ratio_log'] = np.log1p(accidents_population['ratio_accidents_pop'])

    with open(geo_json_data, 'r', encoding='utf-8') as f:
        geojson = json.load(f)

    geojson2 = copy.deepcopy(geojson)

    map_accidents_ratio = folium.Map(
        location=coords,
        tiles=tiles,
        attr=attr,
        zoom_start=5.4
    )

    folium.Choropleth(
        geo_data=geo_json_data,
        data=accidents_population,
        columns=["dep", "ratio_log"],
        key_on="feature.properties.code",
        fill_color='YlOrBr',
        fill_opacity=0.85,
        legend_name='Ratio accidents/population (pour 1000 hab, échelle log)',
        line_weight=1.5,
        bins=8
    ).add_to(map_accidents_ratio)

    for feature in geojson2['features']:
        code = feature['properties']['code']
        row = accidents_population[accidents_population['dep'].astype(str) == str(code)]
        if not row.empty:
            pop_value = row.iloc[0]['population']
            feature['properties']['ratio_accidents'] = round(row.iloc[0]['ratio_accidents_pop'], 2)
            feature['properties']['population'] = int(pop_value) if pandas.notna(pop_value) else 0
            feature['properties']['nb_accidents'] = int(row.iloc[0]['nb_accidents'])
        else:
            feature['properties']['ratio_accidents'] = 0
            feature['properties']['population'] = 0
            feature['properties']['nb_accidents'] = 0

    folium.GeoJson(
        geojson2,
        style_function=lambda feature: {
            'fillColor': 'transparent',
            'fillOpacity': 0,
            'weight': 0,
            'color': 'transparent'
        },
        highlight_function=lambda feature: {
            'fillColor': '#922d50',
            'fillOpacity': 0.6,
            'weight': 2,
            'color': '#3c1b43'
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['nom', 'code', 'ratio_accidents', 'population', 'nb_accidents'],
            aliases=['Département: ', 'Code: ', 'Ratio (acc/1000hab): ', 'Population: ', 'Accidents: '],
            localize=True
        ),
        overlay=True,
        control=False
    ).add_to(map_accidents_ratio)

    return map_accidents_ratio._repr_html_()

