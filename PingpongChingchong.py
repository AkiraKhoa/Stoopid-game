import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 400
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Ping Pong Game")

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up paddles
paddle_width = 10
paddle_height = 60
paddle_speed = 3
paddle_boost_speed = 10
paddle1_x = 50
paddle1_y = window_height // 2 - paddle_height // 2
paddle2_x = window_width - 50 - paddle_width
paddle2_y = window_height // 2 - paddle_height // 2

# Set up ball
ball_radius = 10
ball_speed_x = 3
ball_speed_y = 3
ball_x = window_width // 2
ball_y = window_height // 2

# Set up scores
score1 = 0
score2 = 0
font = pygame.font.Font(None, 36)

# Set up mana and boost delay
mana_max = 100
mana_delay = 200
mana_restore_rate = 0.4
mana1 = mana_max
mana2 = mana_max
mana_timer1 = 0
mana_timer2 = 0

# Set up ball speed increase
ball_speed_increase = 0.2

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move paddles
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle1_y > 0:
        paddle1_y -= paddle_speed
    if keys[pygame.K_s] and paddle1_y < window_height - paddle_height:
        paddle1_y += paddle_speed

    if keys[pygame.K_UP] and paddle2_y > 0:
        paddle2_y -= paddle_speed
    if keys[pygame.K_DOWN] and paddle2_y < window_height - paddle_height:
        paddle2_y += paddle_speed

    # Check paddle boost for player 1
    if keys[pygame.K_SPACE] and mana1 > 0:
        paddle_speed = paddle_boost_speed
        mana1 -= 1
        mana_timer1 = pygame.time.get_ticks()
    else:
        paddle_speed = paddle_speed  # Reset to base speed when the key is not held

    # Check paddle boost for player 2
    if keys[pygame.K_RSHIFT] and mana2 > 0:
        paddle_speed = paddle_boost_speed
        mana2 -= 1
        mana_timer2 = pygame.time.get_ticks()
    else:
        paddle_speed = paddle_speed # Reset to base speed when the key is not held

    # Restore mana after delay
    current_time = pygame.time.get_ticks()
    if current_time - mana_timer1 >= mana_delay and mana1 < mana_max:
               mana1 = min(mana1 + mana_restore_rate, mana_max)
    if current_time - mana_timer2 >= mana_delay and mana2 < mana_max:
        mana2 = min(mana2 + mana_restore_rate, mana_max)

    # Move ball
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Check ball collision with paddles
    if ball_x <= paddle1_x + paddle_width and paddle1_y <= ball_y <= paddle1_y + paddle_height:
        ball_speed_x = abs(ball_speed_x) + ball_speed_increase  # Change ball direction and increase speed
    if ball_x >= paddle2_x - ball_radius and paddle2_y <= ball_y <= paddle2_y + paddle_height:
        ball_speed_x = -abs(ball_speed_x) - ball_speed_increase  # Change ball direction and increase speed

    # Check ball collision with walls
    if ball_y <= 0 or ball_y >= window_height - ball_radius:
        ball_speed_y = -ball_speed_y

    # Check ball out of bounds
    if ball_x < 0:
        score2 += 1
        ball_x = window_width // 2
        ball_y = window_height // 2
        ball_speed_x = random.choice([-3, 3])
        ball_speed_y = random.choice([-3, 3])
    if ball_x > window_width:
        score1 += 1
        ball_x = window_width // 2
        ball_y = window_height // 2
        ball_speed_x = random.choice([-3, 3])
        ball_speed_y = random.choice([-3, 3])

    # Clear the screen
    window.fill(BLACK)

    # Draw paddles
    pygame.draw.rect(window, WHITE, (paddle1_x, paddle1_y, paddle_width, paddle_height))
    pygame.draw.rect(window, WHITE, (paddle2_x, paddle2_y, paddle_width, paddle_height))

    # Draw ball
    pygame.draw.circle(window, WHITE, (int(ball_x), int(ball_y)), ball_radius)

    # Draw scores
    score_text = font.render(f"{score1} - {score2}", True, WHITE)
    window.blit(score_text, (window_width // 2 - score_text.get_width() // 2, 10))

    # Draw mana bars
    pygame.draw.rect(window, WHITE, (10, 10, mana1, 10))
    pygame.draw.rect(window, WHITE, (window_width - 10 - mana2, 10, mana2, 10))

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

    # Check win condition
    if score1 >= 15 or score2 >= 15:
        running = False

# Game over
game_over_text = font.render("Game Over", True, WHITE)
window.blit(game_over_text, (window_width // 2 - game_over_text.get_width() // 2, window_height // 2 - game_over_text.get_height() // 2))
pygame.display.flip()
pygame.time.wait(2000)

# Quit the game
pygame.quit()