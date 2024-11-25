import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

SNAKE_SIZE = 20
SNAKE_SPEED = 10

font = pygame.font.SysFont(None, 55)
small_font = pygame.font.SysFont(None, 35)

music_playing = False
music_button = pygame.Rect(SCREEN_WIDTH - 80, 20, 50, 50)

snake = [(100, 100), (80, 100), (60, 100)]
snake_dir = 'RIGHT'

food = (random.randint(0, SCREEN_WIDTH // SNAKE_SIZE - 1) * SNAKE_SIZE, random.randint(0, SCREEN_HEIGHT // SNAKE_SIZE - 1) * SNAKE_SIZE)

clock = pygame.time.Clock()
high_score = 0
previous_score = 0
game_state = "START"
score = 0
timer = 60
start_ticks = 0
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

def reset_game():
    global snake, snake_dir, food, score, timer, start_ticks
    snake = [(100, 100), (80, 100), (60, 100)]
    snake_dir = 'RIGHT'
    food = (random.randint(0, SCREEN_WIDTH // SNAKE_SIZE - 1) * SNAKE_SIZE, random.randint(0, SCREEN_HEIGHT // SNAKE_SIZE - 1) * SNAKE_SIZE)
    score = 0
    timer = 60
    start_ticks = pygame.time.get_ticks()

def draw_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (30, 20))

def draw_timer():
    timer_text = font.render(f"Time: {timer}", True, WHITE)
    screen.blit(timer_text, (SCREEN_WIDTH // 2 - timer_text.get_width() // 2, 20))

def game_over():
    global high_score, previous_score
    if score > high_score:
        high_score = score
    previous_score = score
    pygame.time.wait(2000)
    game_state = "START"

def start_screen():
    screen.fill(BLACK)
    title_text = font.render("Snake Game", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 3))
    
    start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
    pygame.draw.rect(screen, BLUE, start_button)
    start_button_text = small_font.render("Play", True, WHITE)
    screen.blit(start_button_text, (SCREEN_WIDTH // 2 - start_button_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
    
    high_score_text = small_font.render(f"High Score: {high_score}", True, WHITE)
    previous_score_text = small_font.render(f"Previous Score: {previous_score}", True, WHITE)
    screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 70))
    screen.blit(previous_score_text, (SCREEN_WIDTH // 2 - previous_score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 110))
    
    pygame.display.flip()
    return start_button

running = True
while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if game_state == "START" and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            start_button = start_screen()
            if start_button.collidepoint(mouse_pos):
                game_state = "RUNNING"
                reset_game()

        if event.type == pygame.MOUSEBUTTONDOWN and game_state != "START":
            mouse_pos = event.pos
            if music_button.collidepoint(mouse_pos):
                toggle_music()

    if game_state == "START":
        start_screen()
        draw_music_button()

    elif game_state == "RUNNING":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and snake_dir != 'DOWN':
            snake_dir = 'UP'
        if keys[pygame.K_s] and snake_dir != 'UP':
            snake_dir = 'DOWN'
        if keys[pygame.K_a] and snake_dir != 'RIGHT':
            snake_dir = 'LEFT'
        if keys[pygame.K_d] and snake_dir != 'LEFT':
            snake_dir = 'RIGHT'

        head_x, head_y = snake[0]
        if snake_dir == 'UP':
            head_y -= SNAKE_SIZE
        if snake_dir == 'DOWN':
            head_y += SNAKE_SIZE
        if snake_dir == 'LEFT':
            head_x -= SNAKE_SIZE
        if snake_dir == 'RIGHT':
            head_x += SNAKE_SIZE
        snake = [(head_x, head_y)] + snake[:-1]

        if snake[0] == food:
            snake.append(snake[-1])
            score += 1
            food = (random.randint(0, SCREEN_WIDTH // SNAKE_SIZE - 1) * SNAKE_SIZE, random.randint(0, SCREEN_HEIGHT // SNAKE_SIZE - 1) * SNAKE_SIZE)

        if snake[0] in snake[1:] or head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT:
            game_over()
            game_state = "START"

        screen.fill(BLACK)
        for block in snake:
            pygame.draw.rect(screen, GREEN, (block[0], block[1], SNAKE_SIZE, SNAKE_SIZE))

        pygame.draw.circle(screen, RED, (food[0] + SNAKE_SIZE // 2, food[1] + SNAKE_SIZE // 2), SNAKE_SIZE // 2)

        seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
        timer = 60 - seconds_passed
        if timer <= 0:
            game_over()
            game_state = "START"

        draw_score()
        draw_timer()
        draw_music_button()

    pygame.display.flip()
    clock.tick(SNAKE_SPEED)

pygame.quit()
sys.exit()