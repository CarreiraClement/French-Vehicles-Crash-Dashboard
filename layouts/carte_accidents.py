from dash import html, dcc

from data_utils import load_accidents_all_years, load_departement_names


def carte_accidents_layout():
    accidents = load_accidents_all_years()
    dep_names = load_departement_names()
    deps = sorted(accidents['dep'].dropna().astype(str).str.strip().unique())
    dep_options = []
    for dep in deps:
        code = dep.zfill(2) if dep.isdigit() else dep
        label = dep_names.get(code, dep_names.get(dep, f"Département {dep}"))
        dep_options.append({'label': label, 'value': dep})
    dep_options.append({'label': 'Tous', 'value': 'all'})

    return html.Div([
        html.H1(
            "Carte Interactive des Accidents",
            style={
                'textAlign': 'center',
                'color': '#3c1b43',
                'marginBottom': '15px',
                'marginTop': '0',
                'fontSize': '2em'
            }
        ),

        html.Div([
            html.Div([
                html.Label("Année:", style={'fontWeight': 'bold', 'marginRight': '10px', 'fontSize': '14px', 'display': 'block', 'marginBottom': '5px'}),
                dcc.Slider(
                    id='year-selector-carte',
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
                )
            ], style={'width': '32%', 'display': 'inline-block', 'marginRight': '2%', 'verticalAlign': 'top'}),

            html.Div([
                html.Label("Département:", style={'fontWeight': 'bold', 'marginRight': '10px', 'fontSize': '14px', 'display': 'block', 'marginBottom': '5px'}),
                dcc.Dropdown(
                    id='departement-filter-carte',
                    options=dep_options,
                    value='all',
                    style={'width': '100%'}
                )
            ], style={'width': '32%', 'display': 'inline-block', 'marginRight': '2%', 'verticalAlign': 'top'}),

            html.Div([
                html.Label("Nombre de points:", style={'fontWeight': 'bold', 'marginRight': '10px', 'fontSize': '14px', 'display': 'block', 'marginBottom': '5px'}),
                dcc.Slider(
                    id='max-points-slider',
                    min=1000,
                    max=50000,
                    step=1000,
                    value=10000,
                    marks={
                        1000: {'label': '1K'},
                        5000: {'label': '5K'},
                        10000: {'label': '10K'},
                        20000: {'label': '20K'},
                        30000: {'label': '30K'},
                        40000: {'label': '40K'},
                        50000: {'label': '50K'}
                    },
                    className='year-slider'
                ),
                html.Div(
                    id='max-points-display',
                    style={
                        'textAlign': 'center',
                        'marginTop': '5px',
                        'color': '#3c1b43',
                        'fontWeight': 'bold',
                        'fontSize': '14px'
                    }
                )
            ], style={'width': '32%', 'display': 'inline-block', 'verticalAlign': 'top'})
        ], style={'padding': '15px', 'backgroundColor': '#f5f0e6', 'borderRadius': '10px', 'marginBottom': '15px'}),

        html.Div([
            html.Div([
                dcc.Loading(
                    id='loading-map-points',
                    type='circle',
                    color='#3c1b43',
                    children=html.Iframe(
                        id='map-points-accidents',
                        srcDoc='',
                        style={
                            'width': '100%',
                            'height': 'calc(100vh - 280px)',
                            'border': 'none',
                            'borderRadius': '10px'
                        }
                    )
                )
            ], style={'width': '75%', 'display': 'inline-block', 'verticalAlign': 'top'}),

            html.Div([
                html.Div([
                    html.H4(
                        "Légende",
                        style={
                            'marginTop': '0',
                            'marginBottom': '12px',
                            'color': '#3c1b43',
                            'borderBottom': '2px solid #f87060',
                            'paddingBottom': '6px',
                            'fontSize': '1.2em'
                        }
                    ),
                    html.Div([
                        html.Div([
                            html.Div(
                                style={
                                    'width': '18px',
                                    'height': '18px',
                                    'borderRadius': '50%',
                                    'backgroundColor': '#501537',
                                    'border': '3px solid #501537',
                                    'marginRight': '12px',
                                    'display': 'inline-block'
                                }
                            ),
                            html.Span("Tué", style={'color': '#3c1b43', 'fontSize': '16px'})
                        ], style={'display': 'flex', 'alignItems': 'center', 'margin': '10px 0'}),

                        html.Div([
                            html.Div(
                                style={
                                    'width': '18px',
                                    'height': '18px',
                                    'borderRadius': '50%',
                                    'backgroundColor': '#f87060',
                                    'border': '3px solid #f87060',
                                    'marginRight': '12px',
                                    'display': 'inline-block'
                                }
                            ),
                            html.Span("Blessé hospitalisé", style={'color': '#3c1b43', 'fontSize': '15px'})
                        ], style={'display': 'flex', 'alignItems': 'center', 'margin': '10px 0'}),

                        html.Div([
                            html.Div(
                                style={
                                    'width': '18px',
                                    'height': '18px',
                                    'borderRadius': '50%',
                                    'backgroundColor': '#922d50',
                                    'border': '3px solid #922d50',
                                    'marginRight': '12px',
                                    'display': 'inline-block'
                                }
                            ),
                            html.Span("Blessé léger", style={'color': '#3c1b43', 'fontSize': '15px'})
                        ], style={'display': 'flex', 'alignItems': 'center', 'margin': '10px 0'}),

                        html.Div([
                            html.Div(
                                style={
                                    'width': '18px',
                                    'height': '18px',
                                    'borderRadius': '50%',
                                    'backgroundColor': '#3c1b43',
                                    'border': '3px solid #3c1b43',
                                    'marginRight': '12px',
                                    'display': 'inline-block'
                                }
                            ),
                            html.Span("Indemne", style={'color': '#3c1b43', 'fontSize': '15px'})
                        ], style={'display': 'flex', 'alignItems': 'center', 'margin': '10px 0'}),

                        html.Div([
                            html.Div(
                                style={
                                    'width': '18px',
                                    'height': '18px',
                                    'borderRadius': '50%',
                                    'backgroundColor': '#cccccc',
                                    'border': '3px solid #999999',
                                    'marginRight': '12px',
                                    'display': 'inline-block'
                                }
                            ),
                            html.Span("Non renseigné", style={'color': '#3c1b43', 'fontSize': '15px'})
                        ], style={'display': 'flex', 'alignItems': 'center', 'margin': '10px 0'})
                    ])
                ], style={
                    'padding': '15px',
                    'backgroundColor': '#f5f0e6',
                    'borderRadius': '10px',
                    'border': '2px solid #3c1b43',
                    'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
                    'position': 'sticky',
                    'top': '15px'
                })
            ], style={'width': '22%', 'display': 'inline-block', 'marginLeft': '3%', 'verticalAlign': 'top'})
        ], style={'width': '95%', 'margin': '0 auto', 'height': 'calc(100vh - 200px)'})
    ], style={'height': '100vh', 'overflow': 'hidden'})
