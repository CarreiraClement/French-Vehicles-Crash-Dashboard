from dash import Input, Output
import plotly.express as px

from data_utils import (
    load_accidents_data, load_accidents_all_years,
    load_usagers_data, load_usagers_all_years,
    load_complete_data
)
from config import grav_dict
from Map.map import generate_map_accidents_html, generate_map_ratio_html


def register_home_callbacks(app):
    """Enregistre les callbacks de la page d'accueil."""

    @app.callback(
        Output('accidents-totaux', 'children'),
        Output('usagers-totaux', 'children'),
        Output('deces-totaux', 'children'),
        Output('blesses-totaux', 'children'),
        Input('year-selector', 'value')
    )
    def update_kpi_cards(year):
        year_mapping = {1: 2020, 2: 2021, 3: 2022, 4: 2023}
        if year in (None, 0, 'total'):
            accidents_data = load_accidents_all_years()
            usagers_data = load_usagers_all_years()
        else:
            selected_year = year_mapping.get(int(year), 2023)
            accidents_data = load_accidents_data(selected_year)
            usagers_data = load_usagers_data(selected_year)

        accidents_total = f"{len(accidents_data):,}"
        usagers_total = f"{len(usagers_data):,}"
        deces_total = f"{len(usagers_data[usagers_data['grav'] == 2]):,}"
        blesses_total = f"{len(usagers_data[usagers_data['grav'].isin([3, 4])]):,}"

        return accidents_total, usagers_total, deces_total, blesses_total

    @app.callback(
        Output('graph-gravite', 'figure'),
        Input('departement-filter', 'value')
    )
    def update_gravite(dep_filter):
        dc = load_complete_data(2023)
        dc['grav_lib'] = dc['grav'].map(grav_dict).fillna('Non renseigné')

        if dep_filter != 'all':
            dc = dc[dc['dep'] == dep_filter]

        grav_counts = dc['grav_lib'].value_counts().reset_index()
        grav_counts.columns = ['Gravité', 'Nombre']

        fig = px.pie(
            grav_counts,
            values='Nombre',
            names='Gravité',
            title='Répartition par gravité',
            color_discrete_sequence=['#f87060', '#922d50', '#501537', '#3c1b43']
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        return fig

    @app.callback(
        Output('map-accidents-par-departement', 'srcDoc'),
        Input('type-visualisation', 'value'),
        Input('year-selector', 'value'),
        prevent_initial_call=False
    )
    def update_map_accidents_par_departement(type_visualisation, year):
        if year in (None, 0, 'total'):
            if type_visualisation == 'nombre_accidents':
                return generate_map_accidents_html('total')
            else:
                return generate_map_ratio_html('total')
        else:
            year_mapping = {1: 2020, 2: 2021, 3: 2022, 4: 2023}
            selected_year = year_mapping.get(int(year), 2023)
            if type_visualisation == 'nombre_accidents':
                return generate_map_accidents_html(selected_year)
            else:
                return generate_map_ratio_html(selected_year)
