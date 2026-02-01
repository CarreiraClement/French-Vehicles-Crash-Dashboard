from dash import html, dcc

from data_utils import load_accidents_data, load_departement_names


def home_layout():
    accidents = load_accidents_data(2023)
    dep_names = load_departement_names()

    def dep_label(dep):
        s = str(dep).strip()
        code = s.zfill(2) if s.isdigit() else s
        return dep_names.get(code, dep_names.get(s, f"Département {dep}"))

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
                    options=[{'label': dep_label(dep), 'value': dep}
                             for dep in sorted(accidents['dep'].unique(), key=lambda x: (str(x).zfill(2) if str(x).isdigit() else str(x)))] + [{'label': 'Tous', 'value': 'all'}],
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
