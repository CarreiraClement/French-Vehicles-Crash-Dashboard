from dash import html, dcc


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
