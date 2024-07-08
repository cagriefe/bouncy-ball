import os
import pygame
import pymunk
import pymunk.pygame_util

pygame.init()

WIDTH, HEIGHT = 1000, 1000
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncy Ball")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

FPS = 60
Y_VELOCITY = 100
UP_VELOCITY = 600
DOWN_VELOCITY = 50
BALL_RADIUS = 40
BACKGROUND_COLOR = BLACK
UP_KEY_DELAY = 400

space = pymunk.Space()
space.gravity = (0, 900)

score = 0
font = pygame.font.SysFont('Arial', 30)

def draw_start_menu():
    SCREEN.fill(BLACK)
    font = pygame.font.SysFont('arial', 40)
    title = font.render('My Game', True, WHITE)
    start_button = font.render('Press UP to Start', True, WHITE)
    SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - title.get_height()//2))
    SCREEN.blit(start_button, (WIDTH//2 - start_button.get_width()//2, HEIGHT//2 + start_button.get_height()))
    pygame.display.update()

def draw_game_over_screen():
    SCREEN.fill(BLACK)
    font = pygame.font.SysFont('arial', 40)
    title = font.render('Game Over', True, WHITE)
    restart_button = font.render('R - Restart', True, WHITE)
    quit_button = font.render('Q - Quit', True, WHITE)
    SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - title.get_height()//3))
    SCREEN.blit(restart_button, (WIDTH//2 - restart_button.get_width()//2, HEIGHT//1.9 + restart_button.get_height()))
    SCREEN.blit(quit_button, (WIDTH//2 - quit_button.get_width()//2, HEIGHT//2 + quit_button.get_height()//2))
    pygame.display.update()

def create_ball(position):
    mass = 1
    radius = BALL_RADIUS
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
    body = pymunk.Body(mass, inertia)
    body.position = position
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0.95
    shape.friction = 0.9
    space.add(body, shape)
    return shape

ball = create_ball((500, 500))

last_up_press_time = 0

def handle_ball_movement(keys_pressed, ball_body):
    global last_up_press_time, score
    
    current_time = pygame.time.get_ticks()
    if keys_pressed[pygame.K_LEFT]:
        ball_body.apply_impulse_at_local_point((-Y_VELOCITY, 0))
    if keys_pressed[pygame.K_RIGHT]:
        ball_body.apply_impulse_at_local_point((Y_VELOCITY, 0))
    if keys_pressed[pygame.K_DOWN]:
        ball_body.apply_impulse_at_local_point((0, DOWN_VELOCITY))
    
    if keys_pressed[pygame.K_UP]:
        if current_time - last_up_press_time > UP_KEY_DELAY:
            ball_body.apply_impulse_at_local_point((0, -UP_VELOCITY))
            last_up_press_time = current_time
            score += 1

def draw_window(ball):
    SCREEN.fill(BACKGROUND_COLOR)
    pygame.draw.circle(SCREEN, RED, (int(ball.body.position.x), int(ball.body.position.y)), BALL_RADIUS)
    draw_score()
    pygame.display.update()

def draw_score():
    score_text = font.render(f'Score: {score}', True, WHITE)
    SCREEN.blit(score_text, (10, 10))

def check_boundaries(ball):
    pos = ball.body.position
    if pos.x < BALL_RADIUS or pos.x > WIDTH - BALL_RADIUS or pos.y < BALL_RADIUS or pos.y > HEIGHT - BALL_RADIUS:
        return True
    return False

def main():
    global score
    run = True
    game_state = "start_menu"
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                elif event.key == pygame.K_r and game_state == "game_over":
                    ball.body.position = (500, 500)
                    game_state = "game"
                    score = 0
                elif event.key == pygame.K_q and game_state == "game_over":
                    run = False
                elif event.key == pygame.K_UP and game_state == "start_menu":
                    game_state = "game"
        
        if game_state == "start_menu":
            draw_start_menu()
        elif game_state == "game_over":
            draw_game_over_screen()
        elif game_state == "game":
            keys_pressed = pygame.key.get_pressed()
            handle_ball_movement(keys_pressed, ball.body)
            space.step(1/FPS)
            if check_boundaries(ball):
                game_state = "game_over"
        
        draw_window(ball)
              
    pygame.quit()
    
if __name__ == "__main__":
    main()
    
# arka plan oynasin top yukari cikiyomus gibi ilizyon yapicam
# yanlara platform top yanlardan sekicek