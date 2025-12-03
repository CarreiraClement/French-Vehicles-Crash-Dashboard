from dash import Dash, html, dcc, callback, Output, Input, dash
import plotly.express as px
import pandas as pd

data_vehicles = pd.read_csv('Data/2023/vehicules-2023.csv', sep=';')
data_usagers = pd.read_csv('Data/2023/usagers-2023.csv', sep=';')

app = Dash()

app.layout = [
    html.H1(children="Titre du test", style={"textAlign": "center"}),
    dcc.Dropdown(id='mon-menu', options=[
        {'label': "Nombre d'accident par nombre d'usager", 'value': 'usager'},
    ],value='usager'),
    dcc.Graph(id="graph-content")
]

def ctermine():
    data =  data_usagers['Num_Acc'].value_counts()
    df = data.to_frame(name='nb_personnes')

    df_final = df.groupby('nb_personnes').size().reset_index(name='nb_accidents')
    return df_final

tt = ctermine()


@callback(Output('graph-content', 'figure'),
          Input('mon-menu', 'value'),)
def update_graph(value):
    return px.bar   (tt, x= "nb_personnes", y= "nb_accidents", height=400, range_x=[0, 10])

if __name__ == '__main__':
    app.run(debug=True)
