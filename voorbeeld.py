import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
FPS = 60

# Player attributes
player_width, player_height = 50, 50
player_x, player_y = WIDTH // 2, HEIGHT - player_height
player_vel_y = 0
GRAVITY = 0.5
JUMP_STRENGTH = -10
GROUND = HEIGHT - player_height
player_speed = 5

# Platform
platform = pygame.Rect(200, 510, 200, 10)

# Movement control
is_jumping = False


screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Create a clock object to manage frame rate
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and not is_jumping:  # Jumping mechanic
        player_vel_y = JUMP_STRENGTH
        is_jumping = True
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # Apply gravity
    player_vel_y += GRAVITY
    player_y += player_vel_y

    # Collision with ground
    if player_y >= GROUND:
        player_y = GROUND
        is_jumping = False

    # Collision with platform
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    if player_rect.colliderect(platform) and player_vel_y > 0:
        player_y = platform.top - player_height
        player_vel_y = 0
        is_jumping = False

    # Drawing
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, player_rect)  # Draw player
    pygame.draw.rect(screen, GREEN, platform)    # Draw platform

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
