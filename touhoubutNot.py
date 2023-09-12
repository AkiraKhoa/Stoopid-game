import pygame
import random
import time

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
PLAYER_SIZE = 40
ENEMY_SIZE = 40
BULLET_SIZE = 10
PLAYER_SPEED = 10
BULLET_SPEED = 5
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ENEMY_HEALTH = 3

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Shooting Game")

# Player attributes
player_x = (SCREEN_WIDTH - PLAYER_SIZE) // 2
player_y = (SCREEN_HEIGHT - PLAYER_SIZE) // 2
player_hp = 3

# Lists to store bullets and enemies
bullets = []
enemies = []

# Function to draw the player
def draw_player():
    pygame.draw.polygon(screen, WHITE, [(player_x, player_y + PLAYER_SIZE // 2),
                                       (player_x + PLAYER_SIZE, player_y + PLAYER_SIZE // 2),
                                       (player_x + PLAYER_SIZE // 2, player_y + PLAYER_SIZE)], 0)
    pygame.draw.circle(screen, RED, (player_x + PLAYER_SIZE // 2, player_y + PLAYER_SIZE // 2), BULLET_SIZE // 2)

# Function to draw bullets
def draw_bullets():
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, (bullet[0], bullet[1], BULLET_SIZE, BULLET_SIZE))

# Function to draw enemies
def draw_enemies():
    for enemy in enemies:
        pygame.draw.rect(screen, WHITE, (enemy[0], enemy[1], ENEMY_SIZE, ENEMY_SIZE))

# Updated spawn_enemy function
def spawn_enemy():
    x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
    y = 0  # Spawn enemies at the top of the screen
    enemy_health = ENEMY_HEALTH
    enemies.append([x, y, 0, enemy_health])  # The new 0 represents the initial horizontal enemy movement

# Updated move_objects function
def move_objects():
    global player_x, player_y, player_hp

    # Move bullets and remove them if they go out of screen
    bullets[:] = [(bullet[0] + bullet[2] * BULLET_SPEED, bullet[1] + bullet[3] * BULLET_SPEED, bullet[2], bullet[3])
                  for bullet in bullets if 0 <= bullet[0] < SCREEN_WIDTH and 0 <= bullet[1] < SCREEN_HEIGHT]

    # Move enemies and handle their behavior
    for enemy in enemies:
        enemy[0] += enemy[2] * BULLET_SPEED  # Adjust enemy's x position

        # Update enemy's vertical position to make them move downward
        if enemy[1] < SCREEN_HEIGHT // 2:
            enemy[1] += 1  # Move downward until reaching the bottom half of the screen

        # Check if bullets hit enemies
        for bullet in bullets:
            if enemy[0] < bullet[0] < enemy[0] + ENEMY_SIZE and enemy[1] < bullet[1] < enemy[1] + ENEMY_SIZE:
                enemy[3] -= 1
                bullets.remove(bullet)
                if enemy[3] <= 0:
                    enemies.remove(enemy)

    # Check for player input to move
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_y > 0:
        player_y -= PLAYER_SPEED
    if keys[pygame.K_s] and player_y < SCREEN_HEIGHT - PLAYER_SIZE:
        player_y += PLAYER_SPEED
    if keys[pygame.K_a] and player_x > 0:
        player_x -= PLAYER_SPEED
    if keys[pygame.K_d] and player_x < SCREEN_WIDTH - PLAYER_SIZE:
        player_x += PLAYER_SPEED


# Cooldown timer for player shots
shot_cooldown = 0

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check for player input to shoot with a cooldown
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and shot_cooldown <= 0:
        bullets.append([player_x + PLAYER_SIZE // 2 - BULLET_SIZE // 2,
                        player_y + PLAYER_SIZE // 2 - BULLET_SIZE // 2,
                        0, -1])  # Bullet direction: up
        shot_cooldown = 20  # Set the cooldown timer

    # Update the cooldown timer
    if shot_cooldown > 0:
        shot_cooldown -= 1

    # Spawn enemies randomly
    if random.randint(1, 100) < 20:
        spawn_enemy()

    # Clear the screen
    screen.fill((0, 0, 0))

    # Move and update objects
    move_objects()

    # Draw objects
    draw_player()
    draw_bullets()
    draw_enemies()

    # Check for game over condition
    if player_hp <= 0:
        running = False

    # Update the display
    pygame.display.update()

    # Cap the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
