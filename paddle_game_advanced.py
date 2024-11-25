import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Paddle Ball Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 7

BALL_SIZE = 20
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

user_paddle = pygame.Rect(50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
computer_paddle = pygame.Rect(SCREEN_WIDTH - 60, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 55)
game_over_font = pygame.font.SysFont(None, 75)
start_font = pygame.font.SysFont(None, 75)

player_score = 0

START_SCREEN = 0
GAME_RUNNING = 1
GAME_OVER = 2
game_state = START_SCREEN

music_playing = False
music_button = pygame.Rect(SCREEN_WIDTH - 80, 20, 50, 50)
pygame.mixer.music.load("/Users/pvc/Documents/WixSite Games/paddlegameaudio.wav")

def toggle_music():
    global music_playing
    if music_playing:
        pygame.mixer.music.stop()
        music_playing = False
    else:
        pygame.mixer.music.play(-1)
        music_playing = True

def draw_music_button():
    if music_playing:
        pygame.draw.rect(screen, WHITE, (music_button.x + 10, music_button.y + 10, 10, 30))
        pygame.draw.rect(screen, WHITE, (music_button.x + 30, music_button.y + 10, 10, 30))
    else:
        pygame.draw.polygon(screen, WHITE, [(music_button.x + 15, music_button.y + 10), (music_button.x + 35, music_button.y + 25), (music_button.x + 15, music_button.y + 40)])

def reset_ball():
    ball.x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
    ball.y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2
    global BALL_SPEED_X, BALL_SPEED_Y
    BALL_SPEED_X = random.choice([-5, 5])
    BALL_SPEED_Y = random.choice([-5, 5])

def randomize_ball_movement():
    ball.x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
    ball.y = random.randint(SCREEN_HEIGHT // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 + BALL_SIZE // 2)
    global BALL_SPEED_X, BALL_SPEED_Y
    BALL_SPEED_X = random.choice([-7, -6, -5, -4])
    BALL_SPEED_Y = random.choice([-7, -6, -5, -4, 4, 5, 6, 7])

def draw_score():
    score_text = font.render(f"Score: {player_score}", True, WHITE)
    screen.blit(score_text, (30, 20))

def game_over():
    lose_text = game_over_font.render("You Lose", True, RED)
    screen.blit(lose_text, (SCREEN_WIDTH // 2 - lose_text.get_width() // 2, SCREEN_HEIGHT // 2 - lose_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

def start_screen():
    screen.fill(BLACK)
    start_text = start_font.render("Paddle Ball", True, WHITE)
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 3))
    
    start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
    pygame.draw.rect(screen, BLUE, start_button)
    
    start_button_text = font.render("Start Game", True, WHITE)
    screen.blit(start_button_text, (SCREEN_WIDTH // 2 - start_button_text.get_width() // 2, SCREEN_HEIGHT // 2 + 5))
    
    pygame.display.flip()
    return start_button

running = True
ball_crossed_center = False
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if game_state == START_SCREEN and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            start_button = start_screen()
            if start_button.collidepoint(mouse_pos):
                game_state = GAME_RUNNING
                player_score = 0
                reset_ball()
        
        if event.type == pygame.MOUSEBUTTONDOWN and game_state != GAME_OVER:
            mouse_pos = event.pos
            if music_button.collidepoint(mouse_pos):
                toggle_music()

    if game_state == START_SCREEN:
        start_screen()
        draw_music_button()

    elif game_state == GAME_RUNNING:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and user_paddle.top > 0:
            user_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_s] and user_paddle.bottom < SCREEN_HEIGHT:
            user_paddle.y += PADDLE_SPEED

        if computer_paddle.centery < ball.centery and computer_paddle.bottom < SCREEN_HEIGHT:
            computer_paddle.y += PADDLE_SPEED
        if computer_paddle.centery > ball.centery and computer_paddle.top > 0:
            computer_paddle.y -= PADDLE_SPEED

        ball.x += BALL_SPEED_X
        ball.y += BALL_SPEED_Y

        if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
            BALL_SPEED_Y = -BALL_SPEED_Y

        if ball.colliderect(user_paddle):
            BALL_SPEED_X = -BALL_SPEED_X
            player_score += 1
            ball_crossed_center = False
        elif ball.colliderect(computer_paddle):
            BALL_SPEED_X = -BALL_SPEED_X
            ball_crossed_center = False

        if ball.left <= 0:
            game_state = GAME_OVER
            game_over()
        elif ball.right >= SCREEN_WIDTH:
            reset_ball()

        if ball.x < SCREEN_WIDTH // 2 and BALL_SPEED_X < 0 and not ball_crossed_center:
            randomize_ball_movement()
            ball_crossed_center = True

        pygame.draw.rect(screen, WHITE, user_paddle)
        pygame.draw.rect(screen, WHITE, computer_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))
        draw_score()
        draw_music_button()

    elif game_state == GAME_OVER:
        game_over()
        game_state = START_SCREEN

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()