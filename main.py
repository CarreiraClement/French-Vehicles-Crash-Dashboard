from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
import os

from Map.map import generate_map_accidents_html, generate_map_ratio_html

def load_accidents_data(year):
    file_path = f'Data/{year}/caracteristiques-{year}.csv'
    
    if os.path.exists(file_path):
        return pd.read_csv(file_path, sep=';', low_memory=False)
    
    return pd.DataFrame()

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


app = Dash(__name__)

app.layout = html.Div([
    html.H1(
        "Dashboard des Accidents de la Route en France",
        style={
            'textAlign': 'center',
            'color': '#2c3e50',
            'marginBottom': '30px',
            'fontSize': '2.5em'
        }
    ),
    
    html.Div([
        html.Label("Année:", style={'fontWeight': 'bold', 'marginRight': '10px'}),
        dcc.Dropdown(
            id='year-selector',
            options=[
                {'label': 'Tous', 'value': 'total'},
                {'label': '2020', 'value': 2020},
                {'label': '2021', 'value': 2021},
                {'label': '2022', 'value': 2022},
                {'label': '2023', 'value': 2023}
            ],
            value='total',
            style={'width': '150px', 'display': 'inline-block'}
        )
    ], style={'textAlign': 'center', 'marginBottom': '20px'}),
    
    html.Div([
        html.Div([
            html.H3(id='accidents-totaux', style={'margin': '0', 'fontSize': '2em', 'color': '#e74c3c'}),
            html.P("Accidents totaux", style={'margin': '5px 0', 'color': '#7f8c8d'})
        ], style={
            'width': '24%',
            'display': 'inline-block',
            'textAlign': 'center',
            'padding': '20px',
            'backgroundColor': '#ecf0f1',
            'borderRadius': '10px',
            'margin': '0 0.5%'
        }),
        html.Div([
            html.H3(f"{len(usagers):,}", style={'margin': '0', 'fontSize': '2em', 'color': '#3498db'}),
            html.P("Usagers impliqués", style={'margin': '5px 0', 'color': '#7f8c8d'})
        ], style={
            'width': '24%',
            'display': 'inline-block',
            'textAlign': 'center',
            'padding': '20px',
            'backgroundColor': '#ecf0f1',
            'borderRadius': '10px',
            'margin': '0 0.5%'
        }),
        html.Div([
            html.H3(f"{len(usagers[usagers['grav'] == 2]):,}", style={'margin': '0', 'fontSize': '2em', 'color': '#c0392b'}),
            html.P("Décès", style={'margin': '5px 0', 'color': '#7f8c8d'})
        ], style={
            'width': '24%',
            'display': 'inline-block',
            'textAlign': 'center',
            'padding': '20px',
            'backgroundColor': '#ecf0f1',
            'borderRadius': '10px',
            'margin': '0 0.5%'
        }),
        html.Div([
            html.H3(f"{len(usagers[usagers['grav'].isin([3, 4])]):,}", style={'margin': '0', 'fontSize': '2em', 'color': '#f39c12'}),
            html.P("Blessés", style={'margin': '5px 0', 'color': '#7f8c8d'})
        ], style={
            'width': '24%',
            'display': 'inline-block',
            'textAlign': 'center',
            'padding': '20px',
            'backgroundColor': '#ecf0f1',
            'borderRadius': '10px',
            'margin': '0 0.5%'
        })
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
            dcc.RadioItems(
                id='type-visualisation',
                options=[
                    {'label': 'Nombre d\'accidents', 'value': 'nombre_accidents'},
                    {'label': 'Ratio accidents/population', 'value': 'ratio_accidents_population'}
                ],
                value='nombre_accidents',
                inline=True,
                style={'display': 'inline-block'}
            )
        ], style={'width': '65%', 'display': 'inline-block'})
    ], style={'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '10px', 'marginBottom': '20px'}),
    
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
        ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '2%'}),
    ], style={'marginBottom': '20px'})
])

@callback(
    Output('accidents-totaux', 'children'),
    Input('year-selector', 'value')
)
def update_accidents_totaux(year):
    """Met à jour le nombre d'accidents totaux selon l'année sélectionnée"""
    if year == 'total':
        accidents_data = pd.concat([load_accidents_data(annee) for annee in [2020, 2021, 2022, 2023]])
        return f"{len(accidents_data):,}"
    else:
        accidents_data = load_accidents_data(year)
        return f"{len(accidents_data):,}"

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
        color_discrete_sequence=px.colors.sequential.Reds_r
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400)
    return fig

@callback(
    Output('map-accidents-par-departement', 'srcDoc'),
    Input('type-visualisation', 'value'),
    Input('year-selector', 'value'),
    prevent_initial_call=False
)
def update_map_accidents_par_departement(type_visualisation, year):
    if year == 'total':
        if type_visualisation == 'nombre_accidents':
            return generate_map_accidents_html()
        else:
            return generate_map_ratio_html()
    else:
        if type_visualisation == 'nombre_accidents':
            return generate_map_accidents_html(year)
        else:
            return generate_map_ratio_html(year)

if __name__ == '__main__':
    app.run(debug=True)