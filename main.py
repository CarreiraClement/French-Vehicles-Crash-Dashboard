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


def load_vehicules_data(year):
    file_path = f'Data/{year}/vehicules-{year}.csv'

    if os.path.exists(file_path):
        return pd.read_csv(file_path, sep=';', low_memory=False)

    return pd.DataFrame()


def load_vehicules_all_years(years=None):
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
                dbc.NavLink("Véhicules", href="/vehicules", active="exact", id="nav-vehicules"),
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


def vehicules_layout():
    return html.Div([
        html.H1(
            "Analyse des Véhicules Impliqués dans les Accidents",
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
                    id='vehicules-year-selector',
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
                html.H3(id='vehicules-kpi-total', style={'margin': '0', 'fontSize': '2em', 'color': '#f87060'}),
                html.P("Total Véhicules", style={'margin': '5px 0', 'color': '#3c1b43'})
            ], className='metric-card', style={
                'width': '24%', 'display': 'inline-block', 'textAlign': 'center',
                'padding': '20px', 'borderRadius': '10px', 'margin': '0 0.5%'
            }),
            html.Div([
                html.H3(id='vehicules-kpi-voitures', style={'margin': '0', 'fontSize': '2em', 'color': '#922d50'}),
                html.P("Voitures (VL)", style={'margin': '5px 0', 'color': '#3c1b43'})
            ], className='metric-card', style={
                'width': '24%', 'display': 'inline-block', 'textAlign': 'center',
                'padding': '20px', 'borderRadius': '10px', 'margin': '0 0.5%'
            }),
            html.Div([
                html.H3(id='vehicules-kpi-2roues', style={'margin': '0', 'fontSize': '2em', 'color': '#501537'}),
                html.P("2-Roues motorisés", style={'margin': '5px 0', 'color': '#3c1b43'})
            ], className='metric-card', style={
                'width': '24%', 'display': 'inline-block', 'textAlign': 'center',
                'padding': '20px', 'borderRadius': '10px', 'margin': '0 0.5%'
            }),
            html.Div([
                html.H3(id='vehicules-kpi-velos', style={'margin': '0', 'fontSize': '2em', 'color': '#3c1b43'}),
                html.P("Vélos & EDP", style={'margin': '5px 0', 'color': '#3c1b43'})
            ], className='metric-card', style={
                'width': '24%', 'display': 'inline-block', 'textAlign': 'center',
                'padding': '20px', 'borderRadius': '10px', 'margin': '0 0.5%'
            }),
        ], style={'marginBottom': '30px'}),

        html.Div([
            html.Div([
                dcc.Graph(id='graph-categorie-vehicule')
            ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
            html.Div([
                dcc.Graph(id='graph-motorisation')
            ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        ], style={'marginBottom': '20px'}),

        html.Div([
            html.Div([
                dcc.Graph(id='graph-point-choc')
            ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
            html.Div([
                dcc.Graph(id='graph-obstacle-fixe')
            ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        ], style={'marginBottom': '20px'}),

        html.Div([
            html.Div([
                dcc.Graph(id='graph-evolution-vehicules')
            ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
            html.Div([
                dcc.Graph(id='graph-top-categories')
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

# Dictionnaires pour les véhicules
catv_dict = {
    1: 'Bicyclette',
    2: 'Cyclomoteur <50cm3',
    3: 'Voiturette',
    7: 'VL seul',
    10: 'VU seul 1,5T <= PTAC <= 3,5T',
    13: 'PL seul 3,5T<PTAC<=7,5T',
    14: 'PL seul > 7,5T',
    15: 'PL > 3,5T + remorque',
    16: 'Tracteur routier seul',
    17: 'Tracteur routier + semi-remorque',
    20: 'Engin spécial',
    21: 'Tracteur agricole',
    30: 'Scooter < 50 cm3',
    31: 'Motocyclette > 50 cm3 et <= 125 cm3',
    32: 'Scooter > 50 cm3 et <= 125 cm3',
    33: 'Motocyclette > 125 cm3',
    34: 'Scooter > 125 cm3',
    35: 'Quad léger <= 50 cm3',
    36: 'Quad lourd > 50 cm3',
    37: 'Autobus',
    38: 'Autocar',
    39: 'Train',
    40: 'Tramway',
    41: 'Engin 3 roues à moteur',
    42: 'Engin à déplacement personnel motorisé',
    43: 'Engin à déplacement personnel non motorisé',
    50: 'EDP à moteur',
    60: 'EDP sans moteur',
    80: 'VAE',
    99: 'Autre véhicule'
}

obs_dict = {
    0: 'Non renseigné',
    1: 'Véhicule en stationnement',
    2: 'Arbre',
    3: 'Glissière métallique',
    4: 'Glissière béton',
    5: 'Autre glissière',
    6: 'Bâtiment, mur, pile de pont',
    7: 'Support de signalisation verticale ou poste d\'appel d\'urgence',
    8: 'Poteau',
    9: 'Mobilier urbain',
    10: 'Parapet',
    11: 'Ilot, refuge, borne haute',
    12: 'Bordure de trottoir',
    13: 'Fossé, talus, paroi rocheuse',
    14: 'Autre obstacle fixe sur chaussée',
    15: 'Autre obstacle fixe sur trottoir ou accotement',
    16: 'Sortie de chaussée sans obstacle',
    17: 'Buse-tête d\'aqueduc'
}

choc_dict = {
    0: 'Aucun',
    1: 'Avant',
    2: 'Avant droit',
    3: 'Avant gauche',
    4: 'Arrière',
    5: 'Arrière droit',
    6: 'Arrière gauche',
    7: 'Côté droit',
    8: 'Côté gauche',
    9: 'Chocs multiples (tonneaux)'
}

motor_dict = {
    0: 'Non renseigné',
    1: 'Hydrocarbures',
    2: 'Hybride électrique',
    3: 'Électrique',
    4: 'Hydrogène',
    5: 'Humain',
    6: 'Autre'
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
    elif pathname == '/vehicules':
        return vehicules_layout()
    return home_layout()



@callback(
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
    # VL seul = 7
    voitures = f"{len(vehicules_data[vehicules_data['catv'] == 7]):,}"
    # 2-roues motorisés: cyclomoteurs, motos, scooters (2, 30, 31, 32, 33, 34)
    deux_roues = f"{len(vehicules_data[vehicules_data['catv'].isin([2, 30, 31, 32, 33, 34])]):,}"
    # Vélos et EDP (1, 42, 43, 50, 60, 80)
    velos_edp = f"{len(vehicules_data[vehicules_data['catv'].isin([1, 42, 43, 50, 60, 80])]):,}"

    return total, voitures, deux_roues, velos_edp


@callback(
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


@callback(
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


@callback(
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


@callback(
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

    # Filtrer pour n'afficher que les obstacles réels (pas "Non renseigné")
    vehicules_filtered = vehicules_data[vehicules_data['obs'] != 0]
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


@callback(
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


@callback(
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


if __name__ == '__main__':
    app.run(debug=True)