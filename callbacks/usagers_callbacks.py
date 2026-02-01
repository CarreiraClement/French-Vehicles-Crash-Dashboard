from dash import Input, Output
import pandas as pd
import plotly.express as px

from data_utils import load_usagers_data, load_usagers_all_years
from config import catu_dict, sexe_dict, grav_dict, trajet_dict


def register_usagers_callbacks(app):
    """Enregistre les callbacks de la page usagers."""

    @app.callback(
        Output('usagers-kpi-total', 'children'),
        Output('usagers-kpi-conducteurs', 'children'),
        Output('usagers-kpi-passagers', 'children'),
        Output('usagers-kpi-pietons', 'children'),
        Input('usagers-year-selector', 'value')
    )
    def update_usagers_kpis(year):
        year_mapping = {1: 2020, 2: 2021, 3: 2022, 4: 2023}
        if year in (None, 0, 'total'):
            usagers_data = load_usagers_all_years()
        else:
            selected_year = year_mapping.get(int(year), 2023)
            usagers_data = load_usagers_data(selected_year)

        total = f"{len(usagers_data):,}"
        conducteurs = f"{len(usagers_data[usagers_data['catu'] == 1]):,}"
        passagers = f"{len(usagers_data[usagers_data['catu'] == 2]):,}"
        pietons = f"{len(usagers_data[usagers_data['catu'] == 3]):,}"

        return total, conducteurs, passagers, pietons

    @app.callback(
        Output('graph-categorie-usager', 'figure'),
        Input('usagers-year-selector', 'value')
    )
    def update_graph_categorie(year):
        year_mapping = {1: 2020, 2: 2021, 3: 2022, 4: 2023}
        if year in (None, 0, 'total'):
            usagers_data = load_usagers_all_years()
        else:
            selected_year = year_mapping.get(int(year), 2023)
            usagers_data = load_usagers_data(selected_year)

        usagers_data['catu_lib'] = usagers_data['catu'].map(catu_dict).fillna('Autre')
        cat_counts = usagers_data['catu_lib'].value_counts().reset_index()
        cat_counts.columns = ['Catégorie', 'Nombre']

        fig = px.pie(
            cat_counts,
            values='Nombre',
            names='Catégorie',
            title='Répartition par catégorie d\'usager',
            color_discrete_sequence=['#f87060', '#922d50', '#501537']
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        return fig

    @app.callback(
        Output('graph-sexe-usager', 'figure'),
        Input('usagers-year-selector', 'value')
    )
    def update_graph_sexe(year):
        year_mapping = {1: 2020, 2: 2021, 3: 2022, 4: 2023}
        if year in (None, 0, 'total'):
            usagers_data = load_usagers_all_years()
        else:
            selected_year = year_mapping.get(int(year), 2023)
            usagers_data = load_usagers_data(selected_year)

        usagers_data['sexe_lib'] = usagers_data['sexe'].map(sexe_dict).fillna('Non renseigné')
        sexe_counts = usagers_data['sexe_lib'].value_counts().reset_index()
        sexe_counts.columns = ['Sexe', 'Nombre']

        fig = px.pie(
            sexe_counts,
            values='Nombre',
            names='Sexe',
            title='Répartition par sexe',
            color_discrete_sequence=['#3c1b43', '#f87060']
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        return fig

    @app.callback(
        Output('graph-age-distribution', 'figure'),
        Input('usagers-year-selector', 'value')
    )
    def update_graph_age(year):
        year_mapping = {1: 2020, 2: 2021, 3: 2022, 4: 2023}
        if year in (None, 0, 'total'):
            usagers_data = load_usagers_all_years()
            ref_year = 2023
        else:
            selected_year = year_mapping.get(int(year), 2023)
            usagers_data = load_usagers_data(selected_year)
            ref_year = selected_year

        usagers_data = usagers_data[usagers_data['an_nais'].notna() & (usagers_data['an_nais'] > 1900)]
        usagers_data['age'] = ref_year - usagers_data['an_nais']
        usagers_data = usagers_data[(usagers_data['age'] >= 0) & (usagers_data['age'] <= 110)]

        bins = [0, 18, 25, 35, 45, 55, 65, 75, 120]
        labels = ['0-17', '18-24', '25-34', '35-44', '45-54', '55-64', '65-74', '75+']
        usagers_data['tranche_age'] = pd.cut(usagers_data['age'], bins=bins, labels=labels, right=False)

        age_counts = usagers_data['tranche_age'].value_counts().sort_index().reset_index()
        age_counts.columns = ['Tranche d\'âge', 'Nombre']

        fig = px.bar(
            age_counts,
            x='Tranche d\'âge',
            y='Nombre',
            title='Distribution par tranche d\'âge',
            color='Nombre',
            color_continuous_scale=['#f5f0e6', '#f87060', '#922d50', '#501537']
        )
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        return fig

    @app.callback(
        Output('graph-gravite-par-categorie', 'figure'),
        Input('usagers-year-selector', 'value')
    )
    def update_graph_gravite_categorie(year):
        year_mapping = {1: 2020, 2: 2021, 3: 2022, 4: 2023}
        if year in (None, 0, 'total'):
            usagers_data = load_usagers_all_years()
        else:
            selected_year = year_mapping.get(int(year), 2023)
            usagers_data = load_usagers_data(selected_year)

        usagers_data['catu_lib'] = usagers_data['catu'].map(catu_dict).fillna('Autre')
        usagers_data['grav_lib'] = usagers_data['grav'].map(grav_dict).fillna('Non renseigné')

        grav_cat = usagers_data.groupby(['catu_lib', 'grav_lib']).size().reset_index(name='Nombre')

        fig = px.bar(
            grav_cat,
            x='catu_lib',
            y='Nombre',
            color='grav_lib',
            title='Gravité par catégorie d\'usager',
            barmode='group',
            color_discrete_sequence=['#f87060', '#922d50', '#501537', '#3c1b43']
        )
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title='Catégorie d\'usager',
            yaxis_title='Nombre',
            legend_title='Gravité'
        )
        return fig

    @app.callback(
        Output('graph-motif-trajet', 'figure'),
        Input('usagers-year-selector', 'value')
    )
    def update_graph_motif(year):
        year_mapping = {1: 2020, 2: 2021, 3: 2022, 4: 2023}
        if year in (None, 0, 'total'):
            usagers_data = load_usagers_all_years()
        else:
            selected_year = year_mapping.get(int(year), 2023)
            usagers_data = load_usagers_data(selected_year)

        usagers_data['trajet_lib'] = usagers_data['trajet'].map(trajet_dict).fillna('Non renseigné')
        trajet_counts = usagers_data['trajet_lib'].value_counts().reset_index()
        trajet_counts.columns = ['Motif', 'Nombre']

        fig = px.bar(
            trajet_counts,
            x='Nombre',
            y='Motif',
            title='Motif du trajet',
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
        Output('graph-evolution-annuelle', 'figure'),
        Input('usagers-year-selector', 'value')
    )
    def update_graph_evolution(year):
        years_data = []
        for y in [2020, 2021, 2022, 2023]:
            usagers_data = load_usagers_data(y)
            if not usagers_data.empty:
                total = len(usagers_data)
                tues = len(usagers_data[usagers_data['grav'] == 2])
                blesses = len(usagers_data[usagers_data['grav'].isin([3, 4])])
                years_data.append({'Année': y, 'Total': total, 'Tués': tues, 'Blessés': blesses})

        df_evolution = pd.DataFrame(years_data)

        fig = px.line(
            df_evolution,
            x='Année',
            y=['Total', 'Tués', 'Blessés'],
            title='Évolution annuelle des usagers impliqués',
            markers=True,
            color_discrete_sequence=['#f87060', '#501537', '#922d50']
        )
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(tickmode='linear', dtick=1),
            legend_title='Indicateur'
        )
        return fig
