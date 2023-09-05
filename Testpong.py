import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 1000
window_height = 800
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Simple Pong Game")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
paddle_color = (50, 200, 50)
ball_color = (200, 50, 50)
mana_color = (0, 0, 255)

# Paddle settings
paddle_width = 10
paddle_height = 80
player_paddle = pygame.Rect(50, window_height // 2 - paddle_height // 2, paddle_width, paddle_height)
opponent_paddle = pygame.Rect(window_width - 50 - paddle_width, window_height // 2 - paddle_height // 2, paddle_width, paddle_height)

# Paddle speeds and mana settings
base_paddle_speed = 7
boosted_paddle_speed = 14
player_paddle_speed = base_paddle_speed
opponent_paddle_speed = base_paddle_speed
player_mana = 100
opponent_mana = 100
mana_usage = 1
mana_recharge = 0.5

# Ball settings
ball = pygame.Rect(window_width // 2 - 15, window_height // 2 - 15, 30, 30)
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))

# Scores
player_score = 0
opponent_score = 0
font = pygame.font.Font(None, 50)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Moving the paddles and boosting speed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_paddle.top > 0:
        player_paddle.y -= player_paddle_speed
    if keys[pygame.K_s] and player_paddle.bottom < window_height:
        player_paddle.y += player_paddle_speed
    if keys[pygame.K_a] and player_paddle.left > 0:
        player_paddle.x -= player_paddle_speed
    if keys[pygame.K_d] and player_paddle.right < window_width // 2:
        player_paddle.x += player_paddle_speed
    if keys[pygame.K_SPACE] and player_mana >= mana_usage:
        player_paddle_speed = boosted_paddle_speed
        player_mana -= mana_usage
    else:
        player_paddle_speed = base_paddle_speed
        if player_mana < 100:
            player_mana += mana_recharge
    
    if keys[pygame.K_UP] and opponent_paddle.top > 0:
        opponent_paddle.y -= opponent_paddle_speed
    if keys[pygame.K_DOWN] and opponent_paddle.bottom < window_height:
        opponent_paddle.y += opponent_paddle_speed
    if keys[pygame.K_LEFT] and opponent_paddle.left > window_width // 2:
        opponent_paddle.x -= opponent_paddle_speed
    if keys[pygame.K_RIGHT] and opponent_paddle.right < window_width:
        opponent_paddle.x += opponent_paddle_speed
    if keys[pygame.K_RSHIFT] and opponent_mana >= mana_usage:
        opponent_paddle_speed = boosted_paddle_speed
        opponent_mana -= mana_usage
    else:
        opponent_paddle_speed = base_paddle_speed
        if opponent_mana < 100:
            opponent_mana += mana_recharge

    # Ball movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collisions
    if ball.top <= 0 or ball.bottom >= window_height:
        ball_speed_y = -ball_speed_y
    if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
        ball_speed_x = -ball_speed_x

    # Scoring
    if ball.left <= 0:
        opponent_score += 1
        ball_speed_x = 7
        ball.x = window_width // 2 - ball.width // 2
        ball.y = window_height // 2 - ball.height // 2
    if ball.right >= window_width:
        player_score += 1
        ball_speed_x = -7
        ball.x = window_width // 2 - ball.width // 2
        ball.y = window_height // 2 - ball.height // 2

    # Update the display
    window.fill(black)
    pygame.draw.rect(window, paddle_color, player_paddle)
    pygame.draw.rect(window, paddle_color, opponent_paddle)
    pygame.draw.ellipse(window, ball_color, ball)

    # Draw mana bars
    pygame.draw.rect(window, mana_color, (10, 10, player_mana, 20))
    pygame.draw.rect(window, mana_color, (window_width - opponent_mana - 10, 10, opponent_mana, 20))

    player_text = font.render(str(player_score), True, white)
    opponent_text = font.render(str(opponent_score), True, white)
    window.blit(player_text, (window_width // 4, 50))
    window.blit(opponent_text, (3 * window_width // 4 - opponent_text.get_width(), 50))
    pygame.display.flip()

    pygame.time.Clock().tick(60)
