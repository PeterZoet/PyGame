"""
This script defines levels for a platformer game with the following tile mapping:
    0 - Empty tile
    1 - Underground tile
    2 - Ground tile
    3 - Platform tile
    4 - Player start position
    5-9 - Coins
    10 - Door

Each level:
    - Is 9 tiles tall
    - Is 18 tiles wide
    - Contains one player, one door, and one of each coin (5 to 9).
    - Is structured to be playable, fun, and challenging.

Rules:
    - Row 0 fully empty and the last row filled with underground tiles (1s),
        - only exception are Coins
    - The second to last row contains a mix of 1s and 2s.
    - Directly above the higest underground (1) there must be ground (2)
    - Above ground (2) there may not be ground (2) again
    - Under underground (1) should always be more underground (1), no caves or gaps
    - Under ground (2) there may be no underground (1) anymore and it should be filled with underground (1) untill bottom of screen
    - The door (10) should always be directly on top of ground (2) or a platform (3)
    - Each coin must be reachable by walking over it or jumping to it.
    - Directly above a platform (3) may not be a platform (3)
    - the surface (2's layer) may not be totally flat, make hills or a mountain
"""

level_1 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0],
    [0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 3],
    [0, 0, 0, 0, 0, 0, 0, 3, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 3, 0, 7, 9],
    [0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 3, 0, 3, 0, 0, 0, 2, 2],
    [4, 0, 10, 0, 5, 2, 2, 2, 0, 0, 0, 0, 0, 0, 2, 2, 1, 1],
    [2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

level_2 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 5, 0, 3, 0, 0, 8, 0, 0, 9, 0, 0, 0, 0, 0, 1],
    [1, 4, 0, 3, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 0, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 2, 1],
    [1, 1, 2, 2, 0, 6, 0, 0, 0, 0, 0, 2, 2, 2, 1, 2, 1, 1],
    [1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] 
]


levels = [level_1, level_2]
