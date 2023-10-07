import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BIRD_SIZE = 30
BIRD_COLOR = (255, 255, 0)
PIPE_WIDTH = 70
PIPE_COLOR = (0, 128, 0)  # Green pipes
BACKGROUND_COLOR = (135, 206, 235)  # Sky blue background
GROUND_COLOR = (139, 69, 19)  # Brown ground
GRAVITY = 0.5
JUMP_STRENGTH = 10
PIPE_SPEED = 5
GAP_SIZE = 150

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Define the bird's properties
bird_x = 100
bird_y = SCREEN_HEIGHT // 2
bird_velocity = 0

# Create a list to store pipe positions
pipes = []

# Create a clock object to control the frame rate
clock = pygame.time.Clock()



# Function to draw the bird
def draw_bird(x, y):
    pygame.draw.circle(screen, BIRD_COLOR, (x, y), BIRD_SIZE)

# Function to draw a pipe
def draw_pipe(x, height):
    pygame.draw.rect(screen, PIPE_COLOR, (x, 0, PIPE_WIDTH, height))
    pygame.draw.rect(screen, PIPE_COLOR, (x, height + GAP_SIZE, PIPE_WIDTH, SCREEN_HEIGHT - height - GAP_SIZE))

# Function to draw the ground
def draw_ground():
    pygame.draw.rect(screen, GROUND_COLOR, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))

# Function to restart the game
def restart_game():
    global bird_y, bird_velocity, pipes, score, game_over
    bird_y = SCREEN_HEIGHT // 2
    bird_velocity = 0
    pipes = []
    score = 0
    game_over = False

# Initial game state
score = 0
game_over = False

while True:  # Main game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not game_over:  # Only allow input when the game is not over
            if event.type == pygame.MOUSEBUTTONDOWN:
                bird_velocity = -JUMP_STRENGTH
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird_velocity = -JUMP_STRENGTH

    if not game_over:
        # Move the bird
        bird_velocity += GRAVITY
        bird_y += bird_velocity

        # Generate pipes
        if len(pipes) == 0 or pipes[-1][0] < SCREEN_WIDTH - 200:
            pipe_height = random.randint(50, SCREEN_HEIGHT - 200)
            pipes.append([SCREEN_WIDTH, pipe_height])

        # Move pipes
        for pipe in pipes:
            pipe[0] -= PIPE_SPEED

        # Remove off-screen pipes
        if pipes[0][0] < -PIPE_WIDTH:
            pipes.pop(0)

        # Check for collisions
        for pipe in pipes:
            if bird_x + BIRD_SIZE > pipe[0] and bird_x - BIRD_SIZE < pipe[0] + PIPE_WIDTH:
                if bird_y - BIRD_SIZE < pipe[1] or bird_y + BIRD_SIZE > pipe[1] + GAP_SIZE:
                    game_over = True

        # Check if bird is out of bounds
        if bird_y < 0 or bird_y > SCREEN_HEIGHT:
            game_over = True

        # Update score
        if pipes and pipes[0][0] == bird_x:
            score += 1

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    # Draw pipes
    for pipe in pipes:
        draw_pipe(pipe[0], pipe[1])

    # Draw the bird
    draw_bird(bird_x, bird_y)

    # Draw the ground
    draw_ground()

    # Display the score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

    if game_over:
        # Game over screen
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))

        # Draw the "Restart" button
        restart_font = pygame.font.Font(None, 36)
        restart_text = restart_font.render("Restart", True, (0, 0, 0))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        screen.blit(restart_text, restart_rect)

        pygame.display.flip()

        # Wait for a key press to restart
        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if restart_rect.collidepoint(mouse_x, mouse_y):
                        restart_game()
                        waiting_for_restart = False
