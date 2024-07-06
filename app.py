import os
import pygame
import pymunk
import pymunk.pygame_util

pygame.init()

WIDTH, HEIGHT = 1000, 1000
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncy Ball")
clock = pygame.time.Clock()

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)

FPS = 120
VELOCITY= 50
BALL_RADIUS = 40
BACKGROUND_COLOR= BLACK
x, y = 0, 1

# Pymunk setup
space = pymunk.Space()
space.gravity = (0, 900)

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

def handle_ball_movement(keys_pressed, ball_body):
    if keys_pressed[pygame.K_LEFT]:
            ball_body.apply_impulse_at_local_point((-VELOCITY, 0))
    if keys_pressed[pygame.K_RIGHT]:
            ball_body.apply_impulse_at_local_point((VELOCITY, 0))
    if keys_pressed[pygame.K_UP]:
            ball_body.apply_impulse_at_local_point((0, -VELOCITY))
    if keys_pressed[pygame.K_ESCAPE]:
            ball_body.apply_impulse_at_local_point((0, VELOCITY))

def draw_window(ball):
    SCREEN.fill(BACKGROUND_COLOR)
    pygame.draw.circle(SCREEN, RED, (int(ball.body.position.x), int(ball.body.position.y)), BALL_RADIUS)
    pygame.display.update()
    
def check_boundaries(ball):
    pos = ball.body.position
    if pos.x < BALL_RADIUS or pos.x > WIDTH - BALL_RADIUS or pos.y < BALL_RADIUS or pos.y > HEIGHT - BALL_RADIUS:
        return True
    return False

def main():
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
                    # Reset game state
                    ball.body.position = (500, 500)
                    game_state = "game"
                elif event.key == pygame.K_q and game_state == "game_over":
                    run = False
                elif event.key == pygame.K_UP and game_state == "start_menu":
                    game_state = "game"  # Change game state to "game" when UP key is pressed
        
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