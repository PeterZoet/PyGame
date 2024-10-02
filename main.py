import pygame

pygame.init()

"""
Screen
"""
screen_width = 1800
screen_height = 900
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption('Peters Platformer')
tile_size = 100

"""
constants
"""
fps = 60
timer = pygame.time.Clock()
player_scale = 12
level = [[0 for x in range(18)] for x in range(4)]

#level design test
# 0 is empty tile, 1 is ground, 2 is ground, 3 is platform, 4 is player
level.append([0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2])
level.append([0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,2,1])
level.append([4,0,0,0,0,3,0,0,3,0,0,3,0,0,0,2,1,1])
level.append([2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1])
level.append([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])

print(level)

# loop trough the full list and find where 5 (player) is
for y in range(len(level)):
    if 4 in level[y]:
        start_pos = (level[y].index(4), y)
        print(f"starting pos {start_pos}")

"""
Game variables
"""
player_x = start_pos[0] * tile_size 
player_y = start_pos[1] * tile_size - (12 * player_scale - tile_size) 
# remember initial location for respawn purposes
init_x = player_x
init_y = player_y
counter = 0
mode = 'idle'
direction = 1
player_speed = 12
colliding = False

"""
Load images
"""
background = pygame.transform.scale(pygame.image.load('assets/images/background.png'), (screen_width, screen_height))
ground = pygame.transform.scale(pygame.image.load('assets/images/tiles/ground.png'), (tile_size, tile_size))
underground = pygame.transform.scale(pygame.image.load('assets/images/tiles/underground2.png'), (tile_size, tile_size))
platform = pygame.transform.scale(pygame.image.load('assets/images/tiles/platform.png'), (tile_size, 0.25 * tile_size))
logo = pygame.transform.scale(pygame.image.load('assets/images/logo.png'), (300, 135)) 

player_frames = []
for x in range(4):
    player_frames.append(pygame.transform.scale(pygame.image.load(f'assets/images/player/player_stance_{x+1}.png'), (5 * player_scale, 12 * player_scale)))

 # 0 is empty tile, 1 is underground, 2 is ground, 3 is platform, 4 is player
tiles = ["", underground, ground, platform] # 0 is empty for easier coding later

def draw_player(count, direcection, mod):
    """
    Drawes the player in the game
    :param count: frames in animation
    :param direcection: direction of movement 
    :param mod: idle, walking, maybe more
    """
    if mod != 'idle': # walking
        if direcection == 1: # to right
            screen.blit(player_frames[count // 5], (player_x, player_y))
        else: # to to left
            screen.blit(pygame.transform.flip(player_frames[count // 5], True, False), (player_x, player_y))
    else: # idle
        if direcection == 1: # to right
            screen.blit(player_frames[0], (player_x, player_y))
        else: # to to left
            screen.blit(pygame.transform.flip(player_frames[0], True, False), (player_x, player_y))



def draw_level(level):
    """
    Drawes tiles in the game
    :param level: 2d list of tiles
    """
    # 0 is empty tile, 1 is underground, 2 is ground, 3 is platform, 4 is player
    for x in range(len(level)):
        for y in range(len(level[x])):
            value = level[x][y]
            if 0 < value < 4:
                screen.blit(tiles[value], (y * tile_size, x * tile_size))

def checkCollision(level):
    """
     Check if player is colliding
     Not actual position but visual so it looks good while playing
    :param level: 2d list of tiles
    """
    collide = 0
    
    # hitbox of player
    right_coord = int((player_x + 60) // tile_size)
    left_coord = int(player_x // tile_size)
    top_coord = int((player_y + 30) // tile_size)
    bottom_coord = int((player_y + 80) // tile_size)

    top_right = level[top_coord][right_coord]
    bottom_right = level[bottom_coord][right_coord]
    top_left = level[top_coord][left_coord]
    bottom_left = level[bottom_coord][left_coord]

    # 0 is empty tile, 1 is underground, 2 is ground, 3 is platform, 4 is player

    if top_coord >= 0: # check if player moves higher than screen and top coords collide
        # check if player collides with something on the right or left
        if 0 < top_right < 3 or 0 < bottom_right < 3:
            collide = 1
        elif 0 < top_left < 3 or 0 < bottom_right < 3:
            collide = -1
        else:
            collide = 0
    elif bottom_right >= 0: # check if player moves higher than screen and bottom coords collide
        if 0 < bottom_right < 3:
            collide = 1
        elif 0 < bottom_right < 3:
            collide = -1
        else:
            collide = 0
    else:
        collide = 0

    return collide

"""
Game loop
"""
game_running = True
while game_running:
    
    timer.tick(fps)

    if counter < 19: # counter for frames of player animation
        counter += 1
    else:
        counter = 1

    screen.blit(background, (0,0))
    draw_level(level)
    draw_player(counter, direction, mode)


    # handle player movement
    if mode == 'walk':
        if direction == -1 and player_x > 0 and colliding != -1:
            player_x -= player_speed
        elif direction == 1 and player_x < screen_width - 50 and colliding != 1:
            player_x += player_speed
    colliding = checkCollision(level)

  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction = 1
                mode = 'walk'
            elif event.key == pygame.K_LEFT:
                direction = -1
                mode = 'walk'
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction == 1:
                mode = 'idle'
            elif event.key == pygame.K_LEFT and direction == -1:
                mode = 'idle'

    pygame.display.flip()

# Quit Pygame
pygame.quit()
