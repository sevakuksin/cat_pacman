import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cat Pacman")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 10

# Load cat image
cat_image = pygame.image.load("cat.png")  # Replace with your cat image file
cat_image = pygame.transform.scale(cat_image, (GRID_SIZE, GRID_SIZE))

# Load music
pygame.mixer.init()
pygame.mixer.music.load("meow.mp3")  # Replace with your meow audio file
pygame.mixer.music.play(-1)  # Loop indefinitely

# Cat character
cat = pygame.Rect(WIDTH // 2, HEIGHT // 2, GRID_SIZE, GRID_SIZE)
cat_direction = (0, 0)

# Ghosts
num_ghosts = 3
ghosts = [pygame.Rect(random.randint(0, WIDTH // GRID_SIZE - 1) * GRID_SIZE,
                       random.randint(0, HEIGHT // GRID_SIZE - 1) * GRID_SIZE,
                       GRID_SIZE, GRID_SIZE) for _ in range(num_ghosts)]
ghost_directions = [(0, 0)] * num_ghosts

# Food
foods = [pygame.Rect(random.randint(0, WIDTH // GRID_SIZE - 1) * GRID_SIZE,
                      random.randint(0, HEIGHT // GRID_SIZE - 1) * GRID_SIZE,
                      GRID_SIZE, GRID_SIZE) for _ in range(30)]

# Score
score = 0

# Fonts
font = pygame.font.SysFont(None, 36)

# Movement
def move(rect, direction):
    rect.x += direction[0] * GRID_SIZE
    rect.y += direction[1] * GRID_SIZE
    rect.x %= WIDTH
    rect.y %= HEIGHT

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Control the cat
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        cat_direction = (0, -1)
    if keys[pygame.K_DOWN]:
        cat_direction = (0, 1)
    if keys[pygame.K_LEFT]:
        cat_direction = (-1, 0)
    if keys[pygame.K_RIGHT]:
        cat_direction = (1, 0)

    # Move cat
    move(cat, cat_direction)

    # Move ghosts
    for i in range(num_ghosts):
        if random.random() < 0.2:
            ghost_directions[i] = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        move(ghosts[i], ghost_directions[i])

    # Check collisions with food
    for food in foods[:]:
        if cat.colliderect(food):
            foods.remove(food)
            score += 10

    # Check collisions with ghosts
    for ghost in ghosts:
        if cat.colliderect(ghost):
            running = False

    # Drawing
    screen.fill(BLACK)
    screen.blit(cat_image, (cat.x, cat.y))
    for ghost in ghosts:
        pygame.draw.rect(screen, RED, ghost)
    for food in foods:
        pygame.draw.rect(screen, WHITE, food)

    # Display score
    score_text = font.render(f"Score: {score}", True, BLUE)
    screen.blit(score_text, (10, 10))

    # Update screen
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
