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
HORIZONTAL_VELOCITY = 800
UP_VELOCITY = 300
BALL_RADIUS = 40
BACKGROUND_COLOR = BLACK
UP_KEY_DELAY = 400
PLATFORM_VELOCITY = 100

space = pymunk.Space()
space.gravity = (0, 500)

score = 0
font = pygame.font.SysFont('Arial', 30)
menu_font = pygame.font.SysFont('Arial', 40)

title_text = menu_font.render('Bouncy Ball', True, WHITE)
start_button_text = menu_font.render('Press UP to Start', True, WHITE)
game_over_text = menu_font.render('Game Over', True, WHITE)
restart_button_text = menu_font.render('R - Restart', True, WHITE)
quit_button_text = menu_font.render('Q - Quit', True, WHITE)

def draw_start_menu():
    SCREEN.fill(BLACK)
    SCREEN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - title_text.get_height() // 2))
    SCREEN.blit(start_button_text, (WIDTH // 2 - start_button_text.get_width() // 2, HEIGHT // 2 + start_button_text.get_height()))
    pygame.display.update()

def draw_game_over_screen():
    global score, game_state
    SCREEN.fill(BLACK)
    SCREEN.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 3))
    SCREEN.blit(restart_button_text, (WIDTH // 2 - restart_button_text.get_width() // 2, HEIGHT // 1.9 + restart_button_text.get_height()))
    SCREEN.blit(quit_button_text, (WIDTH // 2 - quit_button_text.get_width() // 2, HEIGHT // 2 + quit_button_text.get_height() // 2))
    pygame.display.update()

def create_ball(position):
    mass = 1
    radius = BALL_RADIUS
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
    body = pymunk.Body(mass, inertia)
    body.position = position
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 1
    shape.friction = 1
    shape.collision_type = 1
    space.add(body, shape)
    return shape

def create_platform(position, size):
    body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    body.position = position
    shape = pymunk.Poly.create_box(body, size)
    shape.elasticity = 1
    shape.friction = 1
    shape.collision_type = 2
    space.add(body, shape)
    return {'body': body, 'size': size, 'initial_position': position}

ball = create_ball((500, 500))
platforms = [
    #create_platform((850, 0), (300, 20)),
    create_platform((150, 150), (300, 20)),
    create_platform((850, 400), (300, 20)),
    create_platform((150, 600), (300, 20)),
    create_platform((850, 900), (300, 20)),
#    create_platform((150, 1000), (300, 20))
]


last_up_press_time = 0

def handle_collision(arbiter, space, data):
    global score
    ball_shape, platform_shape = arbiter.shapes
    
    if ball_shape.collision_type == 1 and platform_shape.collision_type == 2:
        score += 1
#        print(f"Score: {score}")
    
    return True

collision_handler = space.add_collision_handler(1, 2)
collision_handler.data["scored"] = False
collision_handler.pre_solve = handle_collision

def handle_ball_movement(keys_pressed, ball_body):
    global last_up_press_time

    current_time = pygame.time.get_ticks()
    if keys_pressed[pygame.K_LEFT]:
        ball_body.velocity = (-HORIZONTAL_VELOCITY, ball_body.velocity.y)
    elif keys_pressed[pygame.K_RIGHT]:
        ball_body.velocity = (HORIZONTAL_VELOCITY, ball_body.velocity.y)
    else:
        ball_body.velocity = (0, ball_body.velocity.y)

    if keys_pressed[pygame.K_UP]:
        if current_time - last_up_press_time > UP_KEY_DELAY:
            ball_body.apply_impulse_at_local_point((0, -UP_VELOCITY))
            last_up_press_time = current_time

def handle_platform_movement(platforms):
    global HEIGHT, PLATFORM_VELOCITY, score
    
    platform_height = 20  # Assuming the platform height is 20, adjust as per your actual platform size
    
    # Adjust velocity based on score
    if score >= 10:
        PLATFORM_VELOCITY = 120
    if score >= 20:
        PLATFORM_VELOCITY = 140
    if score >= 30:
        PLATFORM_VELOCITY = 160
    if score >= 40:
        PLATFORM_VELOCITY = 170
    if score >= 50:
        PLATFORM_VELOCITY = 180
    if score >= 60:
        PLATFORM_VELOCITY = 190
    if score >= 70:
        PLATFORM_VELOCITY = 200
    if score >= 100:
        PLATFORM_VELOCITY = 240
    if score >= 200:
        PLATFORM_VELOCITY = 300
    
    for platform in platforms:
        platform_body = platform['body']
        platform_y = platform_body.position.y
        
        if platform_y > HEIGHT + platform_height:
            platform_body.position = (platform_body.position.x, -platform['size'][1])  # Reset platform above the screen
        else:
            platform_body.position += pymunk.Vec2d(0, PLATFORM_VELOCITY) / FPS
            
def draw_window(ball):
    SCREEN.fill(BACKGROUND_COLOR)
    pygame.draw.circle(SCREEN, RED, (int(ball.body.position.x), int(ball.body.position.y)), BALL_RADIUS)
    
    for platform in platforms:
        shape = list(platform['body'].shapes)[0]
        vertices = [(v.rotated(shape.body.angle) + shape.body.position) for v in shape.get_vertices()]
        vertices = [(int(vertex.x), int(vertex.y)) for vertex in vertices]
        pygame.draw.polygon(SCREEN, WHITE, vertices)
    
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

def reset_game():
    global score
    score = 0
    ball.body.position = (500, 500)
    ball.body.velocity = (0, 0)

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
                    reset_game()
                    game_state = "start_menu"
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
            handle_platform_movement(platforms)
            space.step(1 / FPS)
            
            if check_boundaries(ball):
                game_state = "game_over"
        
            draw_window(ball)
              
    pygame.quit()

if __name__ == "__main__":
    main()