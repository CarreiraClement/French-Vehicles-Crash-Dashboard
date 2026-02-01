# Configuration et dictionnaires de mapping

# Dictionnaire de gravité
grav_dict = {
    1: 'Indemne',
    2: 'Tué',
    3: 'Blessé hospitalisé',
    4: 'Blessé léger'
}

# Dictionnaires pour les usagers
catu_dict = {1: 'Conducteur', 2: 'Passager', 3: 'Piéton'}
sexe_dict = {1: 'Homme', 2: 'Femme'}
trajet_dict = {
    0: 'Non renseigné',
    1: 'Domicile-travail',
    2: 'Domicile-école',
    3: 'Courses-achats',
    4: 'Utilisation professionnelle',
    5: 'Promenade-loisirs',
    9: 'Autre'
}

# Dictionnaires pour les véhicules
catv_dict = {
    1: 'Bicyclette',
    2: 'Cyclomoteur <50cm3',
    3: 'Voiturette',
    7: 'VL seul',
    10: 'VU seul 1,5T <= PTAC <= 3,5T',
    13: 'PL seul 3,5T<PTAC<=7,5T',
    14: 'PL seul > 7,5T',
    15: 'PL > 3,5T + remorque',
    16: 'Tracteur routier seul',
    17: 'Tracteur routier + semi-remorque',
    20: 'Engin spécial',
    21: 'Tracteur agricole',
    30: 'Scooter < 50 cm3',
    31: 'Motocyclette > 50 cm3 et <= 125 cm3',
    32: 'Scooter > 50 cm3 et <= 125 cm3',
    33: 'Motocyclette > 125 cm3',
    34: 'Scooter > 125 cm3',
    35: 'Quad léger <= 50 cm3',
    36: 'Quad lourd > 50 cm3',
    37: 'Autobus',
    38: 'Autocar',
    39: 'Train',
    40: 'Tramway',
    41: 'Engin 3 roues à moteur',
    42: 'Engin à déplacement personnel motorisé',
    43: 'Engin à déplacement personnel non motorisé',
    50: 'EDP à moteur',
    60: 'EDP sans moteur',
    80: 'VAE',
    99: 'Autre véhicule'
}

obs_dict = {
    0: 'Non renseigné',
    1: 'Véhicule en stationnement',
    2: 'Arbre',
    3: 'Glissière métallique',
    4: 'Glissière béton',
    5: 'Autre glissière',
    6: 'Bâtiment, mur, pile de pont',
    7: 'Support de signalisation verticale ou poste d\'appel d\'urgence',
    8: 'Poteau',
    9: 'Mobilier urbain',
    10: 'Parapet',
    11: 'Ilot, refuge, borne haute',
    12: 'Bordure de trottoir',
    13: 'Fossé, talus, paroi rocheuse',
    14: 'Autre obstacle fixe sur chaussée',
    15: 'Autre obstacle fixe sur trottoir ou accotement',
    16: 'Sortie de chaussée sans obstacle',
    17: 'Buse-tête d\'aqueduc'
}

choc_dict = {
    0: 'Aucun',
    1: 'Avant',
    2: 'Avant droit',
    3: 'Avant gauche',
    4: 'Arrière',
    5: 'Arrière droit',
    6: 'Arrière gauche',
    7: 'Côté droit',
    8: 'Côté gauche',
    9: 'Chocs multiples (tonneaux)'
}

motor_dict = {
    0: 'Non renseigné',
    1: 'Hydrocarbures',
    2: 'Hybride électrique',
    3: 'Électrique',
    4: 'Hydrogène',
    5: 'Humain',
    6: 'Autre'
}

# Années disponibles
AVAILABLE_YEARS = [2020, 2021, 2022, 2023]
