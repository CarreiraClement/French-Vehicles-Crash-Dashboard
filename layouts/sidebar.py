from dash import html
import dash_bootstrap_components as dbc


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
