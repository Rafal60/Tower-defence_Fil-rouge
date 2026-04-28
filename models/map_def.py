"""
Définition de la carte par défaut.
Grille 15x10 : 'G'=grass, 'P'=path, 'S'=spawn, 'B'=base
Le chemin va : spawn (gauche) → droite → bas → gauche → bas → droite → base
"""
 
# Types de cases
G = "grass"
P = "path"
S = "spawn"
B = "base"
 
# Grille 15 colonnes × 10 lignes
DEFAULT_GRID_DEF = [
    [S, P, G, G, G, G, G, G, G, G, G, G, G, G, G],
    [G, P, G, G, G, G, G, G, G, G, G, G, G, G, G],
    [G, P, P, P, P, P, P, P, P, P, P, P, P, G, G],
    [G, G, G, G, G, G, G, G, G, G, G, G, P, G, G],
    [G, G, G, G, G, G, G, G, G, G, G, G, P, G, G],
    [G, G, P, P, P, P, P, P, P, P, P, P, P, G, G],
    [G, G, P, G, G, G, G, G, G, G, G, G, G, G, G],
    [G, G, P, G, G, G, G, G, G, G, G, G, G, G, G],
    [G, G, P, P, P, P, P, P, P, P, P, P, P, P, B],
    [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
]
 
# Waypoints : liste ordonnée de (x, y) que les unités suivent du spawn → base
DEFAULT_WAYPOINTS = [
    (0, 0),   # spawn
    (1, 0),
    (1, 2),
    (12, 2),
    (12, 5),
    (2, 5),
    (2, 8),
    (14, 8),  # base
]
 
SPAWN_POS = (0, 0)
BASE_POS  = (14, 8)
GRID_COLS = 15
GRID_ROWS = 10