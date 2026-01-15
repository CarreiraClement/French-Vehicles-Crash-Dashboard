from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px

from Map.map import generate_map_accidents_html, generate_map_ratio_html


accidents = pd.read_csv('Data/2023/caract-2023.csv', sep=';', low_memory=False)
usagers = pd.read_csv('Data/2023/usagers-2023.csv', sep=';', low_memory=False)
vehicules = pd.read_csv('Data/2023/vehicules-2023.csv', sep=';', low_memory=False)
lieux = pd.read_csv('Data/2023/lieux-2023.csv', sep=';', low_memory=False)
accidents_dep = pd.read_csv('Data/2023/data-store/accidents_par_departement.csv', sep=';', low_memory=False)
accidents_pop = pd.read_csv('Data/2023/data-store/accidents_population_ratio.csv', sep=';', low_memory=False)
departements = pd.read_csv('Data/population/donnees_departements.csv', sep=';', low_memory=False)



data_complete = accidents.merge(usagers, on='Num_Acc', how='left')
data_complete = data_complete.merge(accidents, on='Num_Acc', how='left', suffixes=('', '_acc'))
data_complete = data_complete.merge(vehicules, on=['Num_Acc', 'id_vehicule'], how='left', suffixes=('', '_veh'))
data_complete = data_complete.merge(lieux, on='Num_Acc', how='left', suffixes=('', '_lieu'))
data_complete = data_complete.merge(departements, left_on='dep', right_on="DEP", how='left', suffixes=('', '_dep_info'))
data_complete = data_complete.merge(usagers, on='Num_Acc', how='left', suffixes=('', '_usager'))

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
        "Dashboard des Accidents de la Route en France (2023)",
        style={
            'textAlign': 'center',
            'color': '#2c3e50',
            'marginBottom': '30px',
            'fontSize': '2.5em'
        }
    ),
    
    html.Div([
        html.Div([
            html.H3(f"{len(accidents):,}", style={'margin': '0', 'fontSize': '2em', 'color': '#e74c3c'}),
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
                options=[{'label': f"{dep}", 'value': dep}
                        for dep in sorted(departements['Département'].unique())] + [{'label': 'Tous', 'value': 'all'}],
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
        ], style={'width': '100%', 'display': 'inline-block', 'marginRight': '2%'}),
    ], style={'marginBottom': '20px'}),

    html.Div([
        dcc.Graph(id='histo-nombre-accidents')],
        style={'width': '48%', 'display': 'inline-block'}
    )
])

@callback(
    Output('graph-gravite', 'figure'),
    Input('departement-filter', 'value')
)
def update_gravite(dep_filter):
    dc = data_complete.copy()
    if dep_filter != 'all':
        dc = dc[dc['Département'] == dep_filter]
    
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

def create_age_staircase(data):
    bins = list(range(0, 101, 10))
    labels = [f"{i}-{i+9}" for i in bins[:-1]]

    age_counts = data.groupby("an_nais").size().reset_index(name='Nombre d\'accidents')
    age_counts.columns = ['Âge', 'Nombre d\'accidents']
    age_counts['Âge'] = age_counts['Âge'].apply(lambda x: 2026 - x if pd.notnull(x) else x)
    age_counts['Âge'] = pd.cut(age_counts['Âge'], bins=bins, labels=labels, right=False)
    age_counts = age_counts.groupby('Âge')['Nombre d\'accidents'].sum().reset_index()
    return age_counts

@callback(
    Output('histo-nombre-accidents', 'figure'),
    Input('departement-filter', 'value')
)
def update_nombre_accidents(dep_filter):
    dc = data_complete.copy()
    if dep_filter != 'all':
        dc = dc[dc['dep'] == dep_filter]
    dc = create_age_staircase(dc)
    print(dc)

    fig = px.bar(
        dc,
        x='Âge',
        y='Nombre d\'accidents',
        title='Nombre d\'accidents par département',
        color='Nombre d\'accidents',
        color_continuous_scale=px.colors.sequential.Blues
    )
    fig.update_layout(height=400)
    return fig

@callback(
    Output('map-accidents-par-departement', 'srcDoc'),
    Input('type-visualisation', 'value'),
    prevent_initial_call=False
)
def update_map_accidents_par_departement(type_visualisation):
    if type_visualisation == 'nombre_accidents':
        return generate_map_accidents_html()
    else:
        return generate_map_ratio_html()

if __name__ == '__main__':
    app.run(debug=True)