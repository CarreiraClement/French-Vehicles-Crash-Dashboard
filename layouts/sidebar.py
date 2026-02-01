from dash import html
import dash_bootstrap_components as dbc


sidebar = html.Div(
    [
        html.H2("Analyse des Accidents de la Route en France de 2020 à 2023", className="sidebar-title"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Accueil", href="/", active="exact", id="nav-home"),
                dbc.NavLink("Usagers", href="/usagers", active="exact", id="nav-usagers"),
                dbc.NavLink("Véhicules", href="/vehicules", active="exact", id="nav-vehicules"),
                dbc.NavLink("Carte accidents", href="/carte-accidents", active="exact", id="nav-carte-accidents"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
)
