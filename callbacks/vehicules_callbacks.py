from dash import Input, Output
import pandas as pd
import plotly.express as px

from data_utils import load_vehicules_data, load_vehicules_all_years
from config import catv_dict, obs_dict, choc_dict, motor_dict


def register_vehicules_callbacks(app):
    """Enregistre les callbacks de la page véhicules."""

    @app.callback(
        Output('vehicules-kpi-total', 'children'),
        Output('vehicules-kpi-voitures', 'children'),
        Output('vehicules-kpi-2roues', 'children'),
        Output('vehicules-kpi-velos', 'children'),
        Input('vehicules-year-selector', 'value')
    )
    def update_vehicules_kpis(year):
        year_mapping = {1: 2020, 2: 2021, 3: 2022, 4: 2023}
        if year in (None, 0, 'total'):
            vehicules_data = load_vehicules_all_years()
        else:
            selected_year = year_mapping.get(int(year), 2023)
            vehicules_data = load_vehicules_data(selected_year)

        total = f"{len(vehicules_data):,}"
        voitures = f"{len(vehicules_data[vehicules_data['catv'] == 7]):,}"
        deux_roues = f"{len(vehicules_data[vehicules_data['catv'].isin([2, 30, 31, 32, 33, 34])]):,}"
        velos_edp = f"{len(vehicules_data[vehicules_data['catv'].isin([1, 42, 43, 50, 60, 80])]):,}"

        return total, voitures, deux_roues, velos_edp

    @app.callback(
        Output('graph-categorie-vehicule', 'figure'),
        Input('vehicules-year-selector', 'value')
    )
    def update_graph_categorie_vehicule(year):
        year_mapping = {1: 2020, 2: 2021, 3: 2022, 4: 2023}
        if year in (None, 0, 'total'):
            vehicules_data = load_vehicules_all_years()
        else:
            selected_year = year_mapping.get(int(year), 2023)
            vehicules_data = load_vehicules_data(selected_year)

        vehicules_data['catv_lib'] = vehicules_data['catv'].map(catv_dict).fillna('Autre')
        cat_counts = vehicules_data['catv_lib'].value_counts().head(10).reset_index()
        cat_counts.columns = ['Catégorie', 'Nombre']

        fig = px.pie(
            cat_counts,
            values='Nombre',
            names='Catégorie',
            title='Top 10 - Catégories de véhicules',
            color_discrete_sequence=['#f87060', '#922d50', '#501537', '#3c1b43', '#f5f0e6',
                                      '#d4a574', '#8b4513', '#cd853f', '#deb887', '#bc8f8f']
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        return fig

    @app.callback(
        Output('graph-motorisation', 'figure'),
        Input('vehicules-year-selector', 'value')
    )
    def update_graph_motorisation(year):
        year_mapping = {1: 2020, 2: 2021, 3: 2022, 4: 2023}
        if year in (None, 0, 'total'):
            vehicules_data = load_vehicules_all_years()
        else:
            selected_year = year_mapping.get(int(year), 2023)
            vehicules_data = load_vehicules_data(selected_year)

        vehicules_data['motor_lib'] = vehicules_data['motor'].map(motor_dict).fillna('Non renseigné')
        motor_counts = vehicules_data['motor_lib'].value_counts().reset_index()
        motor_counts.columns = ['Motorisation', 'Nombre']

        fig = px.pie(
            motor_counts,
            values='Nombre',
            names='Motorisation',
            title='Type de motorisation',
            color_discrete_sequence=['#f87060', '#922d50', '#501537', '#3c1b43', '#f5f0e6', '#d4a574']
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        return fig

    @app.callback(
        Output('graph-point-choc', 'figure'),
        Input('vehicules-year-selector', 'value')
    )
    def update_graph_point_choc(year):
        year_mapping = {1: 2020, 2: 2021, 3: 2022, 4: 2023}
        if year in (None, 0, 'total'):
            vehicules_data = load_vehicules_all_years()
        else:
            selected_year = year_mapping.get(int(year), 2023)
            vehicules_data = load_vehicules_data(selected_year)

        vehicules_data['choc_lib'] = vehicules_data['choc'].map(choc_dict).fillna('Non renseigné')
        choc_counts = vehicules_data['choc_lib'].value_counts().reset_index()
        choc_counts.columns = ['Point de choc', 'Nombre']

        fig = px.bar(
            choc_counts,
            x='Nombre',
            y='Point de choc',
            title='Point de choc initial',
            orientation='h',
            color='Nombre',
            color_continuous_scale=['#f5f0e6', '#f87060', '#922d50', '#501537']
        )
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            yaxis={'categoryorder': 'total ascending'}
        )
        return fig

    @app.callback(
        Output('graph-obstacle-fixe', 'figure'),
        Input('vehicules-year-selector', 'value')
    )
    def update_graph_obstacle(year):
        year_mapping = {1: 2020, 2: 2021, 3: 2022, 4: 2023}
        if year in (None, 0, 'total'):
            vehicules_data = load_vehicules_all_years()
        else:
            selected_year = year_mapping.get(int(year), 2023)
            vehicules_data = load_vehicules_data(selected_year)

        vehicules_filtered = vehicules_data[vehicules_data['obs'] != 0].copy()
        vehicules_filtered['obs_lib'] = vehicules_filtered['obs'].map(obs_dict).fillna('Autre')
        obs_counts = vehicules_filtered['obs_lib'].value_counts().head(10).reset_index()
        obs_counts.columns = ['Obstacle', 'Nombre']

        fig = px.bar(
            obs_counts,
            x='Nombre',
            y='Obstacle',
            title='Top 10 - Obstacles fixes heurtés',
            orientation='h',
            color='Nombre',
            color_continuous_scale=['#f5f0e6', '#f87060', '#922d50', '#501537']
        )
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            yaxis={'categoryorder': 'total ascending'}
        )
        return fig

    @app.callback(
        Output('graph-evolution-vehicules', 'figure'),
        Input('vehicules-year-selector', 'value')
    )
    def update_graph_evolution_vehicules(year):
        years_data = []
        for y in [2020, 2021, 2022, 2023]:
            vehicules_data = load_vehicules_data(y)
            if not vehicules_data.empty:
                total = len(vehicules_data)
                voitures = len(vehicules_data[vehicules_data['catv'] == 7])
                deux_roues = len(vehicules_data[vehicules_data['catv'].isin([2, 30, 31, 32, 33, 34])])
                years_data.append({'Année': y, 'Total': total, 'Voitures': voitures, '2-Roues': deux_roues})

        df_evolution = pd.DataFrame(years_data)

        fig = px.line(
            df_evolution,
            x='Année',
            y=['Total', 'Voitures', '2-Roues'],
            title='Évolution annuelle des véhicules impliqués',
            markers=True,
            color_discrete_sequence=['#f87060', '#501537', '#922d50']
        )
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(tickmode='linear', dtick=1),
            legend_title='Type'
        )
        return fig

    @app.callback(
        Output('graph-top-categories', 'figure'),
        Input('vehicules-year-selector', 'value')
    )
    def update_graph_top_categories(year):
        year_mapping = {1: 2020, 2: 2021, 3: 2022, 4: 2023}
        if year in (None, 0, 'total'):
            vehicules_data = load_vehicules_all_years()
        else:
            selected_year = year_mapping.get(int(year), 2023)
            vehicules_data = load_vehicules_data(selected_year)

        vehicules_data['catv_lib'] = vehicules_data['catv'].map(catv_dict).fillna('Autre')
        cat_counts = vehicules_data['catv_lib'].value_counts().head(8).reset_index()
        cat_counts.columns = ['Catégorie', 'Nombre']

        fig = px.bar(
            cat_counts,
            x='Nombre',
            y='Catégorie',
            title='Top 8 - Catégories de véhicules',
            orientation='h',
            color='Nombre',
            color_continuous_scale=['#f5f0e6', '#f87060', '#922d50', '#501537']
        )
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            yaxis={'categoryorder': 'total ascending'}
        )
        return fig
