# Callbacks package
from .home_callbacks import register_home_callbacks
from .usagers_callbacks import register_usagers_callbacks
from .vehicules_callbacks import register_vehicules_callbacks
from .carte_accidents_callbacks import register_carte_accidents_callbacks
from .navigation_callbacks import register_navigation_callbacks


def register_all_callbacks(app):
    register_home_callbacks(app)
    register_usagers_callbacks(app)
    register_vehicules_callbacks(app)
    register_carte_accidents_callbacks(app)
    register_navigation_callbacks(app)
