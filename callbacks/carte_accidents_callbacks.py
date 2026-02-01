from dash import Input, Output

from Map.map import generate_map_points_accidents_html


def register_carte_accidents_callbacks(app):
    """Enregistre les callbacks de la page Carte interactive des accidents."""

    year_mapping = {0: None, 1: 2020, 2: 2021, 3: 2022, 4: 2023}

    @app.callback(
        Output('map-points-accidents', 'srcDoc'),
        Input('year-selector-carte', 'value'),
        Input('departement-filter-carte', 'value'),
        Input('max-points-slider', 'value'),
        prevent_initial_call=False
    )
    def update_map_points(year_val, dep_filter, max_points):
        year = year_mapping.get(year_val, None) if year_val is not None else None
        return generate_map_points_accidents_html(
            year=year,
            dep_filter=dep_filter or 'all',
            max_points=max_points or 10000
        )

    @app.callback(
        Output('max-points-display', 'children'),
        Input('max-points-slider', 'value')
    )
    def update_max_points_display(value):
        if value is None:
            return "10 K points"
        if value >= 1000:
            return f"{value // 1000} K points"
        return f"{value} points"
