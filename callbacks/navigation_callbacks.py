from dash import Input, Output

from layouts.home import home_layout
from layouts.usagers import usagers_layout
from layouts.vehicules import vehicules_layout
from layouts.carte_accidents import carte_accidents_layout


def register_navigation_callbacks(app):
    """Enregistre les callbacks de navigation."""

    @app.callback(
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
        elif pathname == '/carte-accidents':
            return carte_accidents_layout()
        return home_layout()
