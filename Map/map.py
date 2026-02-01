import folium
import pandas
import json
import html as html_module
import numpy as np
from branca.colormap import linear
import copy

import os

from data_utils import (
    load_accidents_all_years,
    load_accidents_data,
    load_usagers_all_years,
    load_usagers_data,
)
from config import grav_dict


GRAV_COLORS = {
    2: '#501537',   
    3: '#f87060',   
    4: '#922d50',   
    1: '#3c1b43',   
    0: '#cccccc',  
}

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
        tiles=tiles,
        attr=attr,
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
            tiles=tiles,
            attr=attr,
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


def generate_map_points_accidents_html(year=None, dep_filter='all', max_points=10000):
    """
    Génère la carte des accidents en points, colorés par gravité (pire issue par accident).
    year: None ou "total" = toutes années, sinon 2020, 2021, 2022, 2023
    dep_filter: "all" ou code département
    max_points: nombre max de points affichés
    """
    if year is None or year == "total" or year == 0:
        accidents_data = load_accidents_all_years()
        usagers_data = load_usagers_all_years()
    else:
        accidents_data = load_accidents_data(year)
        usagers_data = load_usagers_data(year)

    if accidents_data.empty or usagers_data.empty:
        map_obj = folium.Map(
            location=coords,
            tiles=tiles,
            attr=attr,
            zoom_start=6
        )
        return map_obj._repr_html_()


    usagers_grav = usagers_data[['Num_Acc', 'grav']].copy()
    usagers_grav['grav'] = pandas.to_numeric(usagers_grav['grav'], errors='coerce').fillna(0).astype(int)
    usagers_grav['grav'] = usagers_grav['grav'].replace(0, 5)
    worst_grav = usagers_grav.groupby('Num_Acc')['grav'].min()
    worst_grav = worst_grav.replace(5, 0)

    accidents_with_grav = accidents_data.merge(
        worst_grav.rename('grav_accident'),
        on='Num_Acc',
        how='left'
    )
    accidents_with_grav['grav_accident'] = accidents_with_grav['grav_accident'].fillna(0).astype(int)

    if dep_filter != 'all':
        dep_str = str(dep_filter).strip()
        accidents_with_grav = accidents_with_grav[
            accidents_with_grav['dep'].astype(str).str.strip() == dep_str
        ]


    for col in ['lat', 'long']:
        if col in accidents_with_grav.columns:
            accidents_with_grav[col] = pandas.to_numeric(
                accidents_with_grav[col].astype(str).str.replace(',', '.', regex=False),
                errors='coerce'
            )

    points = accidents_with_grav.dropna(subset=['lat', 'long']).copy()
    points = points[(points['lat'] >= -90) & (points['lat'] <= 90) &
                    (points['long'] >= -180) & (points['long'] <= 180)]

    if points.empty:
        map_obj = folium.Map(
            location=coords,
            tiles=tiles,
            attr=attr,
            zoom_start=6
        )
        return map_obj._repr_html_()

    if len(points) > max_points:
        points = points.sample(n=max_points, random_state=42)

    map_obj = folium.Map(
        location=coords,
        tiles=tiles,
        attr=attr,
        zoom_start=5.4
    )

    for _, row in points.iterrows():
        grav = int(row['grav_accident'])
        color = GRAV_COLORS.get(grav, GRAV_COLORS[0])
        grav_label = grav_dict.get(grav, 'Non renseigné')
        try:
            j, m, a = row.get('jour'), row.get('mois'), row.get('an')
            if pandas.notna(j) and pandas.notna(m) and pandas.notna(a):
                date_str = f"{int(float(j)):02d}/{int(float(m)):02d}/{int(float(a))}"
            else:
                date_str = "—"
        except (TypeError, ValueError):
            date_str = "—"
        heure = row.get('hrmn', '') if pandas.notna(row.get('hrmn')) else "—"
        dep = row.get('dep', '') if pandas.notna(row.get('dep')) else "—"
        adr_raw = row.get('adr', '')
        adr = html_module.escape(str(adr_raw).strip()) if pandas.notna(adr_raw) and str(adr_raw).strip() else ""
        popup_lines = [
            f"<b>Date</b> : {date_str}",
            f"<b>Heure</b> : {html_module.escape(str(heure))}",
            f"<b>Département</b> : {html_module.escape(str(dep))}",
            f"<b>Gravité</b> : {html_module.escape(grav_label)}",
        ]
        if adr:
            popup_lines.append(f"<b>Lieu</b> : {adr}")
        popup_html = "<br>".join(popup_lines)
        popup = folium.Popup(popup_html, max_width=280, min_width=200)
        folium.CircleMarker(
            location=[row['lat'], row['long']],
            radius=4,
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.8,
            weight=2,
            popup=popup,
        ).add_to(map_obj)

    return map_obj._repr_html_()
