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
player_scale = 14
level = [[0 for x in range(18)] for x in range(6)]

#level design
# 0 is empty tile, 1 is underground, 2 is ground, 3 is platform, 4 is player
level.append([4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
level.append([1 for x in range(18)])
level.append([2 for x in range(18)])

"""
Load images
"""
background = pygame.transform.scale(pygame.image.load('assets/images/background.png'), (screen_width, screen_height))
ground = pygame.transform.scale(pygame.image.load('assets/images/tiles/ground.png'), (tile_size, tile_size))
underground = pygame.transform.scale(pygame.image.load('assets/images/tiles/underground.png'), (tile_size, tile_size))
platform = pygame.transform.scale(pygame.image.load('assets/images/tiles/platform.png'), (tile_size, 0.25 * tile_size))
logo = pygame.transform.scale(pygame.image.load('assets/images/logo.png'), (300, 135)) 
player_frames = []
for x in range(4):
    player_frames.append(pygame.transform.scale(pygame.image.load(f'assets/images/player/player_stance_{x+1}.png'), (5 * player_scale, 8 * player_scale)))

tiles = ["", ground, underground, platform] # 0 is empty for easier coding later

def draw_level(level):
    """
    Drawes tiles in the game
    """
    # 0 is empty tile, 1 is underground, 2 is ground, 3 is platform, 4 is player
    for x in range(len(level)):
        for y in range(len(level[x])):
            value = level[x][y]
            if 0 < value < 4:
                screen.blit(tiles[value], (y * tile_size, x * tile_size))



"""
Game loop
"""
game_running = True
while game_running:
    
    timer.tick(fps)
    screen.blit(background, (0,0))
    draw_level(level)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
    pygame.display.flip()

# Quit Pygame
pygame.quit()
