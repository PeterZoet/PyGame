import pygame
from levels import *

pygame.init()

pygame.mixer.music.load('assets/audio/retro-8bit-happy-videogame-music-246631.mp3')  
pygame.mixer.music.play(-1)

"""
Screen settings
"""
screen_width = 1800
screen_height = 900
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption('Knowledge Quest; A BaseCamp Adventure')
tile_size = 100

"""
Constants
"""
fps = 60
player_scale = 12
timer = pygame.time.Clock()

"""
Game variables
"""
inventory = [False, False, False, False, False]
player_speed = 10
jump_height = 15
gravity = 1
active_level = 0

"""
Load images
"""
background = pygame.transform.scale(pygame.image.load('assets/images/background.png'), (screen_width, screen_height))
level_one_wall = pygame.transform.scale(pygame.image.load('assets/images/level_one_wall.png'), (screen_width, screen_height))
ground = pygame.transform.scale(pygame.image.load('assets/images/tiles/ground.png'), (tile_size, tile_size))
level_one_ground = pygame.transform.scale(pygame.image.load('assets/images/tiles/level_one_ground.png'), (tile_size, tile_size))
underground = pygame.transform.scale(pygame.image.load('assets/images/tiles/underground2.png'), (tile_size, tile_size))
new_underground = pygame.transform.scale(pygame.image.load('assets/images/tiles/new_underground.png'), (tile_size, tile_size))
platform = pygame.transform.scale(pygame.image.load('assets/images/tiles/platform.png'), (tile_size, 0.6 * tile_size))
stone_platform = pygame.transform.scale(pygame.image.load('assets/images/tiles/vines_platform.png'), (tile_size, tile_size))
door = pygame.transform.scale(pygame.image.load('assets/images/door.png'), (tile_size, tile_size))
new_door = pygame.transform.scale(pygame.image.load('assets/images/new_door.png'), (tile_size, tile_size))
lock = pygame.transform.scale(pygame.image.load('assets/images/lock.png'), (tile_size, tile_size))
new_lock = pygame.transform.scale(pygame.image.load('assets/images/new_lock.png'), (tile_size, tile_size))
knowledge = [pygame.transform.scale(pygame.image.load('assets/images/knowledge.png'), (tile_size, tile_size)) for _ in range(5)]
new_knowledge = [pygame.transform.scale(pygame.image.load('assets/images/new_knowledge.png'), (tile_size, tile_size)) for _ in range(5)]
logo = pygame.transform.scale(pygame.image.load('assets/images/logo.png'), (300, 300))

player_frames = [
    pygame.transform.scale(pygame.image.load(f'assets/images/player/stance_{x + 1}_player.png'), (5.5 * player_scale, 9.2 * player_scale))
    for x in range(11)
]

tiles = ["", new_underground, level_one_ground, stone_platform]


def play_knowledge_collected_sound():
    """
    Play the soundeffect of collecting knwoledge (a coin) once
    """
    effect = pygame.mixer.Sound('assets/audio/coin-pickup-98269.mp3')  
    effect.play()


def play_door_sound():
    """
    Play the soundeffect of going trough a door once
    """
    effect = pygame.mixer.Sound('assets/audio/dorm-door-opening-6038.mp3')  
    effect.play()

def play_jump_sound():
    """
    Play the soundeffect of jumping into the air
    """
    effect = pygame.mixer.Sound('assets/audio/retro-jump-3-236683.mp3')  
    effect.play()



def load_level(active_level: int) -> list[list[int]]:
    """
    Create a list of list wit digits that represent certain entities

    :return: a level filled with digits representing assets
    """
    # from levels.py
    level = levels[active_level]
    return level


def find_player_start(level: list[list[int]]) -> tuple[int, int]:
    """
    Loop trough the level and find player starting position

    :param level: the list of digits
    :return: the x and y coord of the players start position
    """
    for _ in range(len(level)):
        if 4 in level[_]:
            return (_, level[_].index(4))
    return (0, 0)


def show_menu():
    """
    Present a menu to the user, options:
    - Press ENTER to start
    - Press ESC to quit
    """
    main_menu_background = pygame.transform.scale(pygame.image.load("assets/images/new_main_menu_background.jpg"), (screen_width, screen_height))
    menu_running = True
    while menu_running:
        screen.blit(main_menu_background, (0, 0))
        font = pygame.font.SysFont(None, 94)
        title_surface = font.render("Knowledge Quest; A BaseCamp Adventure", True, (196, 45, 69))
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


def draw_player(count: int, direction: int, mode: str, x: int, y: int):
    """
    Draw the player on the screen,load the correct image for the animation

    :param count: frame of the animation
    :param direction: player direction, left or right
    :param mode: stance of the player
    :param x: x coord of player
    :param y: y coord of player
    """
    if mode != 'idle':
        frame = player_frames[count // 5]
        frame = pygame.transform.flip(frame, True, False) if direction == -1 else frame
        screen.blit(frame, (x, y))
    else:
        frame = pygame.transform.flip(player_frames[0], True, False) if direction == -1 else player_frames[0]
        screen.blit(frame, (x, y))
        

def draw_level(level: list[list[int]]):
    """
    draw the level on the screen load the correct image based on value of tile

    -   Game components
        -   0 is empty tile
        -   1 is underground
        -   2 is ground
        -   3 is platform
        -   4 is player
        -   5-9 is knowlegde
        -   10 is door

    :param level: list of list, contains values of tiles
    """
    for x in range(len(level)):
        for y in range(len(level[x])):
            value = level[x][y]
            if 0 < value < 4:
                screen.blit(tiles[value], (y * tile_size, x * tile_size))
            elif 5 <= value <= 9:
                if not inventory[value - 5]:
                    screen.blit(new_knowledge[value - 5], (y * tile_size, x * tile_size))
            elif value == 10:
                screen.blit(new_door, (y * tile_size, x * tile_size))
                if not all(inventory):
                    screen.blit(new_lock, (y * tile_size, x * tile_size))
                if all(inventory):
                    play_door_sound()


def draw_inventory():   
    """
    Visualizes the inventory
    """
    font = pygame.font.SysFont(None, 30)
    pygame.draw.rect(screen, 'black', [5, screen_height - 120, screen_width - 10, 110], 0, 5)
    pygame.draw.rect(screen, (196, 45, 69), [5, screen_height - 120, screen_width - 10, 110], 3, 5)
    pygame.draw.rect(screen, 'white', [8, screen_height - 117, 420, 104], 1, 5)
    pygame.draw.rect(screen, 'white', [428, screen_height - 117, 872, 104], 1, 5)
    pygame.draw.rect(screen, 'white', [880, screen_height - 117, 910, 104], 1, 5)
    font.italic = True
    inventory_text = font.render('Inventory:', True, 'white')
    screen.blit(inventory_text, (14, screen_height - 113))
    for _ in range(5):
        pygame.draw.rect(screen, (196, 45, 69), [15 + (80 * _), screen_height - 88, 70, 70], 5, 5)
        if inventory[_]:
            scaled_knowledge = pygame.transform.scale(knowledge[_], (55, 55))
            screen.blit(scaled_knowledge, (25 + (80 * _), screen_height - 88))


def check_collision(level: list[list[int]], player_x: int, player_y: int):
    """
    Check if player is colliding
    Not actual position but visual so it looks good while playing

    :param level: 2d list of tiles
    """
    collide = False
    
    # hitbox of player
    right_coord = int((player_x + 50) // tile_size)
    left_coord = int(player_x // tile_size)
    top_coord = int((player_y + 10) // tile_size)
    bottom_coord = int((player_y + 100) // tile_size)

    # pygame.draw.circle(screen, (  255,   0, 0), (player_x + 50, player_y + 10), 5) #top right
    # pygame.draw.circle(screen, (  255,   0, 0), (player_x, player_y + 10), 5) #top left
    # pygame.draw.circle(screen, (  255,   0, 0), (player_x + 50, player_y + 100), 5) #bottom right
    # pygame.draw.circle(screen, (  255,   0, 0), (player_x, player_y + 100), 5) #bottom left


    top_right = level[top_coord][right_coord]
    bottom_right = level[bottom_coord][right_coord]
    top_left = level[top_coord][left_coord]
    bottom_left = level[bottom_coord][left_coord]

    # 0 is empty tile, 1 is underground, 2 is ground, 3 is platform, 4 is player, 5-9 is knowlegde, 10 is door

    if top_coord >= 0: # check if player moves higher than screen and top coords collide
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
            play_knowledge_collected_sound()
    elif 5 <= top_right <= 9: 
        if not inventory[top_right - 5]:
            inventory[top_right - 5] = True
            play_knowledge_collected_sound()
    elif 5 <= bottom_left <= 9: 
        if not inventory[top_right - 5]:
            inventory[bottom_left - 5] = True
            play_knowledge_collected_sound()
    elif 5 <= bottom_right <= 9: 
        if not inventory[top_right - 5]:
            inventory[bottom_right - 5] = True
            play_knowledge_collected_sound()

 
          
    return collide


def check_verticals(level: list[list[int]], player_x: int, player_y: int):
    """
    Check if player should fall or stay on tile
    Not actual position but visual so it looks good while playing
    :param y_pos: player y position
    """
    center_coord = int((player_x + 30) // 100)
    bottom_coord = int((player_y + 110) // 100)
    # pygame.draw.circle(screen, (  0,   255, 0), (player_x + 30, player_y + 110), 5)

    # 0 is empty tile, 1 is underground, 2 is ground, 3 is platform, 4 is player, 5 is knowledge 
    if player_y + 110 > 0: # if full player is in level
        if 0 < level[bottom_coord][center_coord] <  4: # ground, underground or platform
            falling = False
        else:
            falling = True
    else:
        falling = True
    if not falling: # compensate for falling trough a tile
        player_y = (bottom_coord - 1) * 100 - 10 # 1 compensates for gravity/jump_height

    return falling, player_y


def game_loop(level: list[list[int]], start_pos: tuple[int, int]):
    """
    The loop of the game, it runs on 60 fps.

    :param level: 2d list of tiles
    :param start_pos: player starting position
    """
    player_x = start_pos[1] * 100
    player_y = start_pos[0] * 100 - ( 8 * player_scale - 100)
    counter = 0
    direction =  1
    y_change = 0
    mode = 'idle'
    in_air = False
    colliding = False
    
    while True:
        timer.tick(fps)

        if counter < 19:
            counter += 1
        else:
            counter = 0 

        screen.blit(level_one_wall, (0,0))
        draw_level(level)
        draw_player(counter, direction, mode, player_x, player_y)
        draw_inventory()
        colliding = check_collision(level, player_x, player_y)
        
        if mode == 'walk':
            if direction == -1 and player_x > 0 and colliding != -1:
                player_x -= player_speed
            elif direction == 1 and player_x < screen_width - 60 and colliding != 1:
                player_x += player_speed

        if in_air:
            y_change -= gravity
            player_y -= y_change
        in_air, player_y = check_verticals(level, player_x, player_y)
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
                    play_jump_sound()
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_RIGHT, pygame.K_LEFT):
                    mode = 'idle'

        pygame.display.flip()


def main():
    level = load_level(active_level)
    start_pos = find_player_start(level)
    show_menu()
    game_loop(level, start_pos)


if __name__ == "__main__":
    main()
