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

##BALL_1_IMAGE = pygame.image.load(os.path.join('assets', 'ball1.webp'))
##BALL_1 = pygame.transform.scale(BALL_1_IMAGE, (BALL_WIDTH, BALL_HEIGHT))

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
##    ball = pygame.Rect(158, 600, BALL_WIDTH, BALL_HEIGHT)
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False
        
        keys_pressed = pygame.key.get_pressed()
        handle_ball_movement(keys_pressed, ball.body)
         
        space.step(1/FPS)
        
        
        if check_boundaries(ball):
            run = False
        
        draw_window(ball)
              
    pygame.quit()
    
if __name__ == "__main__":
    main()