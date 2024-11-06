import pygame

# Initialize pygame
pygame.init()

# Screen settings
screen_width = 1800
screen_height = 900
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption('Platformer')
tile_size = 100

# Constants
fps = 60
player_scale = 12
timer = pygame.time.Clock()

# Game variables
inventory = [False, False, False, False, False]
player_speed = 12
jump_height = 20
gravity =  1

# Load images
background = pygame.transform.scale(pygame.image.load('assets/images/background.png'), (screen_width, screen_height))
ground = pygame.transform.scale(pygame.image.load('assets/images/tiles/ground.png'), (tile_size, tile_size))
underground = pygame.transform.scale(pygame.image.load('assets/images/tiles/underground2.png'), (tile_size, tile_size))
platform = pygame.transform.scale(pygame.image.load('assets/images/tiles/platform.png'), (tile_size, 0.25 * tile_size))
door = pygame.transform.scale(pygame.image.load('assets/images/door.png'), (tile_size, tile_size))
lock = pygame.transform.scale(pygame.image.load('assets/images/lock.png'), (tile_size, tile_size))
knowledge = [pygame.transform.scale(pygame.image.load('assets/images/knowledge.png'), (tile_size, tile_size)) for _ in range(5)]
logo = pygame.transform.scale(pygame.image.load('assets/images/logo.png'), (300, 300))
newplayer = pygame.transform.scale(pygame.image.load('assets/images/player/new_design_0.png'), (8 * player_scale, 10 * player_scale))
# player_frames = [
#     pygame.transform.scale(pygame.image.load(f'assets/images/player/player_stance_{x+1}.png'), (5 * player_scale, 12 * player_scale))
#     for x in range(4)
# ]
tiles = ["", underground, ground, platform]

def load_level():
    """
    Create a list of list wit digits that represent certain entities

    :return: a level filled with entities
    """
    level = [[0 for x in range(18)] for x in range(3)]
    level += [
        [0,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [0,0,0,0,3,6,0,0,0,7,0,0,0,0,0,8,2,1],
        [4,0,10,0,0,3,0,0,0,3,0,9,0,3,0,2,1,1],
        [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    ]
    return level


def find_player_start(level: list) -> tuple[int, int]:
    """
    Loop trough the level and find player starting position

    :param level: the list of digits that represent entities
    :return: the x and y coord of the players start position
    """
    for y in range(len(level)):
        if 4 in level[y]:
            return (level[y].index(4), y)
    return (0, 0)


def show_menu():
    """
    !Zeiler deze toevoegen!
    """
    main_menu_background = pygame.transform.scale(pygame.image.load("assets/images/new_main_menu_background.jpg"), (screen_width, screen_height))
    menu_running = True
    while menu_running:
        screen.blit(main_menu_background, (0, 0))
        font = pygame.font.SysFont(None, 74)
        title_surface = font.render("", True, (255, 255, 255))
        start_surface = font.render("", True, (255, 255, 255))
        exit_surface = font.render("", True, (255, 255, 255))
        screen.blit(title_surface, (screen_width // 2 - title_surface.get_width() // 2, screen_height // 2 - 100))
        screen.blit(start_surface, (screen_width // 2 - start_surface.get_width() // 2, screen_height // 2))
        screen.blit(exit_surface, (screen_width // 2 - exit_surface.get_width() // 2, screen_height // 2 + 100))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu_running = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
        pygame.display.flip()


def draw_player(direction, mode, x, y):
    """
    Draw the player on the screen,load the correct image for the animation

    :param count: frame of the animation
    :param direction: player direction, left or right
    :param mode: stance of the player
    :param x: x coord of player
    :param y: y coord of player
    """
    if mode != 'idle':
        # frame = player_frames[count // 5]
        frame = pygame.transform.flip(newplayer, True, False) if direction == -1 else newplayer
        screen.blit(newplayer, (x, y))
    else:
        frame = pygame.transform.flip(newplayer, True, False) if direction == -1 else newplayer
        screen.blit(newplayer, (x, y))
        

def draw_level(level):
    """
    draw the level on the screen load the correct image based on value of tile

    :param level: list of list, contains values of tiles
    """
    for x in range(len(level)):
        for y in range(len(level[x])):
            value = level[x][y]
            if 0 < value < 4:
                screen.blit(tiles[value], (y * tile_size, x * tile_size))
            elif 5 <= value <= 9:
                if not inventory[value - 5]:
                    screen.blit(knowledge[value - 5], (y * tile_size, x * tile_size))
            elif value == 10:
                screen.blit(door, (y * tile_size, x * tile_size))
                if not all(inventory):
                    screen.blit(lock, (y * tile_size, x * tile_size))


def check_collision(level, player_x, player_y):
    """
    Check if player is colliding
    Not actual position but visual so it looks good while playing
    :param level: 2d list of tiles
    """
    collide = False
    
    # hitbox of player
    right_coord = int((player_x + 60) // tile_size)
    left_coord = int(player_x // tile_size)
    top_coord = int((player_y + 30) // tile_size)
    bottom_coord = int((player_y + 104) // tile_size)
    
    top_right = level[top_coord][right_coord]
    bottom_right = level[bottom_coord][right_coord]
    top_left = level[top_coord][left_coord]
    bottom_left = level[bottom_coord][left_coord]

    # 0 is empty tile, 1 is underground, 2 is ground, 3 is platform, 4 is player

    if top_coord >= 0: # check if player moves higher than screen and top coords collide
        # check if player collides with something on the right or left
        if 0 < top_right < 3 or 0 < bottom_right < 3:
            collide = 1
        elif 0 < top_left < 3 or 0 < bottom_left < 3:
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

    if 5 <= top_left <= 9: # when colliding with knowledge
        if not inventory[top_left - 5]:
            inventory[top_left - 5] = True
    elif 5 <= top_right <= 9: 
        if not inventory[top_right - 5]:
            inventory[top_right - 5] = True
    elif 5 <= bottom_left <= 9: 
        if not inventory[top_right - 5]:
            inventory[bottom_left - 5] = True
    elif 5 <= bottom_right <= 9: 
        if not inventory[top_right - 5]:
            inventory[bottom_right - 5] = True



    return collide

# check feet collision on landings
def check_verticals(level, player_x, player_y):
    """
    Check if player should fall or stay on tile
    Not actual position but visual so it looks good while playing
    :param y_pos: player y position
    """
    center_coord = int((player_x + 45) // tile_size)
    bottom_coord = int((player_y + 105) // tile_size)
    # pygame.draw.circle(screen, (  0,   255, 0), (player_x + 25, player_y + 105), 5)
    
    # top_coord_platform = int((player_y + 240) // tile_size)
    # pygame.draw.circle(screen, (  255,   0, 0), (player_x + 25, player_y + 240), 5)

    # bottom_coord_platform = int((player_y + 40) // tile_size)
    # pygame.draw.circle(screen, (  0,   0, 255), (player_x + 25, player_y + 40), 5)

    # 0 is empty tile, 1 is underground, 2 is ground, 3 is platform, 4 is player, 5 is knowledge 
    # VROEGER PLAYER_Y + 110 > 0
    if player_y + 110 > 0: # if full player is in level
        if 0 < level[bottom_coord][center_coord] <  4: # ground or underground
            falling = False
        # elif level[bottom_coord_platform][center_coord] == 3: # platform
        #     falling = False
        else:
            falling = True
    else:
        falling = True
    if not falling: # compensate for falling trough a tile
        player_y = (bottom_coord - 1) * 100 - 6

    return falling, player_y



def game_loop(level, start_pos):
    """
    The loop of the game, it runs on 60 fps.

    :param level: 2d list of tiles
    :param start_pos: player starting position
    """
    x, y = start_pos[0] * tile_size, start_pos[1] * tile_size - (12 * player_scale - tile_size)
    direction, mode, in_air = 1, 'idle', False
    # counter = 0
    y_change, colliding = 0, False
    
    while True:
        timer.tick(fps)
 #       counter = (counter + 1) % 20
        screen.blit(background, (0,0))
        draw_level(level)
        draw_player(direction, mode, x, y)
        colliding = check_collision(level, x, y)
        
        if mode == 'walk':
            if direction == -1 and x > 0 and colliding != -1:
                x -= player_speed
            elif direction == 1 and x < screen_width - 50 and colliding != 1:
                x += player_speed

        if in_air:
            y_change -= gravity
            y -= y_change
        in_air, y = check_verticals(level, x, y)
        if not in_air:
            y_change = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    direction, mode = 1, 'walk'
                elif event.key == pygame.K_LEFT:
                    direction, mode = -1, 'walk'
                elif event.key in (pygame.K_SPACE, pygame.K_UP) and not in_air:
                    in_air, y_change = True, jump_height
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_RIGHT, pygame.K_LEFT):
                    mode = 'idle'

        pygame.display.flip()

def main():
    level = load_level()
    start_pos = find_player_start(level)
    show_menu()
    game_loop(level, start_pos)

if __name__ == "__main__":
    main()
