import folium
import pandas
import json
import numpy as np
from branca.colormap import linear
import copy

coords = (48.8398094,2.5840685)
geo_json_data = 'Data/geojson/departements.geojson'
accidents_data = pandas.read_csv('Data/2023/caract-2023.csv', sep=';')
accident_by_department = accidents_data.groupby('dep').size().reset_index(name='nb_accidents')

accident_by_department.to_csv('Data/2023/data-store/accidents_par_departement.csv', sep=';', index=False, encoding='utf-8')

accidents_from_csv = pandas.read_csv('Data/2023/data-store/accidents_par_departement.csv', sep=';')

with open(geo_json_data, 'r', encoding='utf-8') as f:
    geojson = json.load(f)

accidents_dict = dict(zip(accidents_from_csv['dep'].astype(str), accidents_from_csv['nb_accidents']))

accident_by_department['nb_accidents_log'] = np.log1p(accident_by_department['nb_accidents'])

map = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=6)

folium.Choropleth(
    geo_data=geo_json_data,
    data=accident_by_department,
    columns=["dep", "nb_accidents_log"],
    key_on="feature.properties.code",
    fill_color='YlOrRd',
    fill_opacity=0.8,
    legend_name='Nombre d\'accidents par département',
    line_weight=2,
    bins=8
).add_to(map)

for feature in geojson['features']:
    code = feature['properties']['code']
    feature['properties']['nb_accidents'] = accidents_dict.get(code, 0)

folium.GeoJson(
    geojson,
    style_function=lambda feature: {'fillColor': 'transparent', 'fillOpacity': 0, 'weight': 0, 'color': 'transparent'},
    highlight_function=lambda feature: {
        'fillColor': 'green',
        'fillOpacity': 0.5,
        'weight': 2,
        'color': 'green'
    },
    tooltip=folium.GeoJsonTooltip(
        fields=['nom', 'code', 'nb_accidents'],
        aliases=['Département: ', 'Code: ', 'Nombre d\'accidents: '],
        localize=True
    ),
    overlay=True,
    control=False
).add_to(map)

map.save(outfile='map.html')

population_data = pandas.read_csv('Data/population/donnees_departements.csv', sep=';')

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

accidents_population.to_csv('Data/2023/data-store/accidents_population_ratio.csv', sep=';', index=False, encoding='utf-8')

import copy
geojson2 = copy.deepcopy(geojson)

map2 = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=6)

folium.Choropleth(
    geo_data=geo_json_data,
    data=accidents_population,
    columns=["dep", "ratio_log"],
    key_on="feature.properties.code",
    fill_color='YlOrRd',
    fill_opacity=0.8,
    legend_name='Ratio accidents/population (pour 1000 hab, échelle log)',
    line_weight=2,
    bins=8
).add_to(map2)

for feature in geojson2['features']:
    code = feature['properties']['code']
    row = accidents_population[accidents_population['dep'].astype(str) == code]
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
    style_function=lambda feature: {'fillColor': 'transparent', 'fillOpacity': 0, 'weight': 0, 'color': 'transparent'},
    highlight_function=lambda feature: {
        'fillColor': 'blue',
        'fillOpacity': 0.5,
        'weight': 2,
        'color': 'blue'
    },
    tooltip=folium.GeoJsonTooltip(
        fields=['nom', 'code', 'ratio_accidents', 'population', 'nb_accidents'],
        aliases=['Département: ', 'Code: ', 'Ratio (acc/1000hab): ', 'Population: ', 'Accidents: '],
        localize=True
    ),
    overlay=True,
    control=False
).add_to(map2)

map2.save(outfile='map_ratio.html')