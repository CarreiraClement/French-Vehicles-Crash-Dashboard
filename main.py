from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import os

from Map.map import generate_map_accidents_html, generate_map_ratio_html
from data_utils import load_accidents_all_years


def load_accidents_data(year):
    file_path = f'Data/{year}/caracteristiques-{year}.csv'

    if os.path.exists(file_path):
        return pd.read_csv(file_path, sep=';', low_memory=False)

    return pd.DataFrame()


def load_usagers_data(year):
    file_path = f'Data/{year}/usagers-{year}.csv'

    if os.path.exists(file_path):
        return pd.read_csv(file_path, sep=';', low_memory=False)

    return pd.DataFrame()


def load_usagers_all_years(years=None):
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

accidents = pd.read_csv('Data/2023/caracteristiques-2023.csv', sep=';', low_memory=False)
usagers = pd.read_csv('Data/2023/usagers-2023.csv', sep=';', low_memory=False)
vehicules = pd.read_csv('Data/2023/vehicules-2023.csv', sep=';', low_memory=False)
lieux = pd.read_csv('Data/2023/lieux-2023.csv', sep=';', low_memory=False)
accidents_dep = pd.read_csv('Data/2023/data-store/accidents_par_departement.csv', sep=';', low_memory=False)
accidents_pop = pd.read_csv('Data/2023/data-store/accidents_population_ratio.csv', sep=';', low_memory=False)


data_complete = accidents.merge(usagers, on='Num_Acc', how='left')
data_complete = data_complete.merge(vehicules, on=['Num_Acc', 'id_vehicule'], how='left', suffixes=('', '_veh'))
data_complete = data_complete.merge(lieux, on='Num_Acc', how='left', suffixes=('', '_lieu'))


grav_dict = {
    1: 'Indemne',
    2: 'Tué',
    3: 'Blessé hospitalisé',
    4: 'Blessé léger'
}

data_complete['grav_lib'] = data_complete['grav'].map(grav_dict).fillna('Non renseigné')


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)


sidebar = html.Div(
    [
        html.H2("Accidents FR", className="sidebar-title"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact", id="nav-home"),
                dbc.NavLink("Usagers", href="/usagers", active="exact", id="nav-usagers"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
)


def home_layout():
    return html.Div([
        html.H1(
            "Dashboard des Accidents de la Route en France",
            style={
                'textAlign': 'center',
                'color': '#3c1b43',  
                'marginBottom': '30px',
                'fontSize': '2.5em'
            }
        ),

        html.Div([
            html.Label("Année:", style={'fontWeight': 'bold', 'marginRight': '10px'}),
            html.Div(
                dcc.Slider(
                    id='year-selector',
                    min=0,
                    max=4,
                    step=1,
                    value=0,
                    marks={
                        0: {'label': 'Tous', 'style': {'color': '#3c1b43', 'fontWeight': '600'}},
                        1: {'label': '2020'},
                        2: {'label': '2021'},
                        3: {'label': '2022'},
                        4: {'label': '2023'},
                    },
                    className='year-slider'
                ),
                style={'width': '60%', 'margin': '0 auto'}
            )
        ], style={'marginBottom': '30px'}),

        html.Div([
            html.Div([
                html.Div(
                    className='metric-value',
                    children=dcc.Loading(
                        id='accidents-totaux-loading',
                        type='circle',
                        color='#f87060',
                        children=html.H3(
                            id='accidents-totaux',
                            style={'margin': '0', 'fontSize': '2em', 'color': '#f87060'}
                        )
                    )
                ),
                html.P("Accidents totaux", style={'margin': '5px 0', 'color': '#3c1b43'})
            ], className='metric-card', style={
                'width': '24%',
                'display': 'inline-block',
                'textAlign': 'center',
                'padding': '20px',
                'borderRadius': '10px',
                'margin': '0 0.5%'
            }),
            html.Div([
                html.Div(
                    className='metric-value',
                    children=dcc.Loading(
                        id='usagers-totaux-loading',
                        type='circle',
                        color='#922d50',
                        children=html.H3(
                            id='usagers-totaux',
                            style={'margin': '0', 'fontSize': '2em', 'color': '#922d50'}
                        )
                    )
                ),
                html.P("Usagers impliqués", style={'margin': '5px 0', 'color': '#3c1b43'})
            ], className='metric-card', style={
                'width': '24%',
                'display': 'inline-block',
                'textAlign': 'center',
                'padding': '20px',
                'borderRadius': '10px',
                'margin': '0 0.5%'
            }),
            html.Div([
                html.Div(
                    className='metric-value',
                    children=dcc.Loading(
                        id='blesses-totaux-loading',
                        type='circle',
                        color='#501537ff',
                        children=html.H3(
                            id='blesses-totaux',
                            style={'margin': '0', 'fontSize': '2em', 'color': '#501537ff'}
                        )
                    )
                ),
                html.P("Blessés", style={'margin': '5px 0', 'color': '#3c1b43'})
            ], className='metric-card', style={
                'width': '24%',
                'display': 'inline-block',
                'textAlign': 'center',
                'padding': '20px',
                'borderRadius': '10px',
                'margin': '0 0.5%'
            }),
            html.Div([
                html.Div(
                    className='metric-value',
                    children=dcc.Loading(
                        id='deces-totaux-loading',
                        type='circle',
                        color='#501537',
                        children=html.H3(
                            id='deces-totaux',
                            style={'margin': '0', 'fontSize': '2em', 'color': '#501537'}
                        )
                    )
                ),
                html.P("Décès", style={'margin': '5px 0', 'color': '#3c1b43'})
            ], className='metric-card', style={
                'width': '24%',
                'display': 'inline-block',
                'textAlign': 'center',
                'padding': '20px',
                'borderRadius': '10px',
                'margin': '0 0.5%'
            }),
        ], style={'marginBottom': '30px'}),

        html.Div([
            html.Div([
                html.Label("Filtre par département:", style={'fontWeight': 'bold', 'marginRight': '10px'}),
                dcc.Dropdown(
                    id='departement-filter',
                    options=[{'label': f"Département {dep}", 'value': dep}
                             for dep in sorted(accidents['dep'].unique())] + [{'label': 'Tous', 'value': 'all'}],
                    value='all',
                    style={'width': '200px'}
                )
            ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '20px'}),
            html.Div([
                html.Label("Type de visualisation:", style={'fontWeight': 'bold', 'marginRight': '10px'}),
                dcc.Dropdown(
                    id='type-visualisation',
                    options=[
                        {'label': 'Ratio accidents/population', 'value': 'ratio_accidents_population'},
                        {'label': "Nombre d'accidents", 'value': 'nombre_accidents'}
                    ],
                    value='ratio_accidents_population',
                    style={'width': '300px'}
                )
            ], style={'width': '65%', 'display': 'inline-block'})
        ], style={'padding': '20px', 'backgroundColor': '#f5f0e6', 'borderRadius': '10px', 'marginBottom': '20px'}),

        html.Div([
            html.Iframe(
                id='map-accidents-par-departement',
                srcDoc='',
                style={
                    'width': '100%',
                    'height': '600px',
                    'border': 'none',
                    'borderRadius': '10px'
                }
            )
        ], style={'width': '90%', 'margin': '0 auto', 'marginBottom': '30px'}),

        html.Div([
            html.Div([
                dcc.Graph(id='graph-gravite')
            ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '2%', 'padding': '20px'}),
        ], style={'marginBottom': '20px'})
    ])


def usagers_layout():
    return html.Div([
        html.H1(
            "Analyse des Usagers Impliqués dans les Accidents",
            style={
                'textAlign': 'center',
                'color': '#3c1b43',
                'marginBottom': '30px',
                'fontSize': '2.5em'
            }
        ),

        html.Div([
            html.Label("Année:", style={'fontWeight': 'bold', 'marginRight': '10px'}),
            html.Div(
                dcc.Slider(
                    id='usagers-year-selector',
                    min=0,
                    max=4,
                    step=1,
                    value=0,
                    marks={
                        0: {'label': 'Tous', 'style': {'color': '#3c1b43', 'fontWeight': '600'}},
                        1: {'label': '2020'},
                        2: {'label': '2021'},
                        3: {'label': '2022'},
                        4: {'label': '2023'},
                    },
                    className='year-slider'
                ),
                style={'width': '60%', 'margin': '0 auto'}
            )
        ], style={'marginBottom': '30px'}),

        html.Div([
            html.Div([
                html.H3(id='usagers-kpi-total', style={'margin': '0', 'fontSize': '2em', 'color': '#f87060'}),
                html.P("Total Usagers", style={'margin': '5px 0', 'color': '#3c1b43'})
            ], className='metric-card', style={
                'width': '24%', 'display': 'inline-block', 'textAlign': 'center',
                'padding': '20px', 'borderRadius': '10px', 'margin': '0 0.5%'
            }),
            html.Div([
                html.H3(id='usagers-kpi-conducteurs', style={'margin': '0', 'fontSize': '2em', 'color': '#922d50'}),
                html.P("Conducteurs", style={'margin': '5px 0', 'color': '#3c1b43'})
            ], className='metric-card', style={
                'width': '24%', 'display': 'inline-block', 'textAlign': 'center',
                'padding': '20px', 'borderRadius': '10px', 'margin': '0 0.5%'
            }),
            html.Div([
                html.H3(id='usagers-kpi-passagers', style={'margin': '0', 'fontSize': '2em', 'color': '#501537'}),
                html.P("Passagers", style={'margin': '5px 0', 'color': '#3c1b43'})
            ], className='metric-card', style={
                'width': '24%', 'display': 'inline-block', 'textAlign': 'center',
                'padding': '20px', 'borderRadius': '10px', 'margin': '0 0.5%'
            }),
            html.Div([
                html.H3(id='usagers-kpi-pietons', style={'margin': '0', 'fontSize': '2em', 'color': '#3c1b43'}),
                html.P("Piétons", style={'margin': '5px 0', 'color': '#3c1b43'})
            ], className='metric-card', style={
                'width': '24%', 'display': 'inline-block', 'textAlign': 'center',
                'padding': '20px', 'borderRadius': '10px', 'margin': '0 0.5%'
            }),
        ], style={'marginBottom': '30px'}),

        html.Div([
            html.Div([
                dcc.Graph(id='graph-categorie-usager')
            ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
            html.Div([
                dcc.Graph(id='graph-sexe-usager')
            ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        ], style={'marginBottom': '20px'}),

        html.Div([
            html.Div([
                dcc.Graph(id='graph-age-distribution')
            ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
            html.Div([
                dcc.Graph(id='graph-gravite-par-categorie')
            ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        ], style={'marginBottom': '20px'}),

        html.Div([
            html.Div([
                dcc.Graph(id='graph-motif-trajet')
            ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
            html.Div([
                dcc.Graph(id='graph-evolution-annuelle')
            ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        ], style={'marginBottom': '20px'}),
    ])


app.layout = html.Div([
    dcc.Location(id='url'),
    sidebar,
    html.Div(id='page-content', className='content')
])


@callback(
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
    else:
        selected_year = year_mapping.get(int(year), 2023)
        accidents_data = load_accidents_data(selected_year)

    if year in (None, 0, 'total'):
        usagers_data = load_usagers_all_years()
    else:
        selected_year = year_mapping.get(int(year), 2023)
        usagers_data = load_usagers_data(selected_year)

    accidents_total = f"{len(accidents_data):,}"
    usagers_total = f"{len(usagers_data):,}"
    deces_total = f"{len(usagers_data[usagers_data['grav'] == 2]):,}"
    blesses_total = f"{len(usagers_data[usagers_data['grav'].isin([3, 4])]):,}"

    return accidents_total, usagers_total, deces_total, blesses_total

@callback(
    Output('graph-gravite', 'figure'),
    Input('departement-filter', 'value')
)
def update_gravite(dep_filter):
    dc = data_complete.copy()
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

@callback(
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


catu_dict = {1: 'Conducteur', 2: 'Passager', 3: 'Piéton'}
sexe_dict = {1: 'Homme', 2: 'Femme'}
trajet_dict = {
    0: 'Non renseigné',
    1: 'Domicile-travail',
    2: 'Domicile-école',
    3: 'Courses-achats',
    4: 'Utilisation professionnelle',
    5: 'Promenade-loisirs',
    9: 'Autre'
}


@callback(
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


@callback(
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


@callback(
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


@callback(
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


@callback(
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


@callback(
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


@callback(
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


@callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname in ['/', '/home', None]:
        return home_layout()
    elif pathname == '/usagers':
        return usagers_layout()
    return home_layout()

if __name__ == '__main__':
    app.run(debug=True)