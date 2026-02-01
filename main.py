
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

from layouts.sidebar import sidebar
from callbacks import register_all_callbacks


app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

app.layout = html.Div([
    dcc.Location(id='url'),
    sidebar,
    html.Div(id='page-content', className='content')
])

register_all_callbacks(app)


if __name__ == '__main__':
    app.run(debug=True)

