import os
import pygame

WIDTH, HEIGHT = 393, 852
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncy Ball")
clock = pygame.time.Clock()

WHITE = (255,255,255)
BLACK = (0,0,0)

FPS = 120
VELOCITY= 3

BALL_WIDTH, BALL_HEIGHT = 80,80

BALL_1_IMAGE = pygame.image.load(os.path.join('assets', 'ball1.webp'))
BALL_1 = pygame.transform.scale(BALL_1_IMAGE, (BALL_WIDTH, BALL_HEIGHT))

def handle_ball_movement(keys_pressed, ball):
    if keys_pressed[pygame.K_LEFT]:
            ball.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT]:
            ball.x += VELOCITY
    if keys_pressed[pygame.K_UP]:
            ball.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN]:
            ball.y += VELOCITY

def draw_window(ball):
    SCREEN.fill(WHITE)
    SCREEN.blit(BALL_1, (ball.x, ball.y))
    pygame.display.update()

def main():
    ball = pygame.Rect(158, 600, BALL_WIDTH, BALL_HEIGHT)
    
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  
        
        keys_pressed = pygame.key.get_pressed()
        handle_ball_movement(keys_pressed, ball)
       
        
        draw_window(ball)
              
    pygame.quit()
    
if __name__ == "__main__":
    main()