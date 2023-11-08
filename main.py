import cv2
import mediapipe
import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
SNAKE_SPEED = 0.1
GREEN_SQUARE_DURATION = 1.0  # Initial duration in seconds
FOOD_DURATION = 5.0  # Food duration in seconds
FOOD_COLOR = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Initialize snake variables
snake = [pygame.math.Vector2(WIDTH // 2, HEIGHT // 2)]
snake_direction = pygame.math.Vector2(0, -1)  # Initial direction (up)

# Initialize timer for green squares
last_green_square_time = time.time()
green_squares = []
green_square_timers = []

# Initialize food variables
food_position = pygame.math.Vector2(random.randint(0, WIDTH - 20), random.randint(0, HEIGHT - 20))
food_timer = time.time()

# Indicator variables
indicator_radius = 10
indicator_color = RED

# Frame counter for controlling circle spawning
frame_counter = 0

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get the position of the mouse cursor
    mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())

    # Calculate the direction vector based on cursor's position relative to the screen center
    center = pygame.math.Vector2(WIDTH // 2, HEIGHT // 2)
    direction_to_cursor = (mouse_pos - center)

    # Normalize the direction vector only if its length is not zero
    if direction_to_cursor.length() > 0:
        direction_to_cursor.normalize_ip()

    # Update the snake's direction
    snake_direction = direction_to_cursor

    # Update the snake's position
    snake[0] += snake_direction * SNAKE_SPEED

    # Check for collision with the screen boundaries
    if snake[0].x < 0 or snake[0].x >= WIDTH or snake[0].y < 0 or snake[0].y >= HEIGHT:
        pygame.quit()
        sys.exit()

    # Check for food collision
    if snake[0].distance_to(food_position) < 20:
        food_position = pygame.math.Vector2(random.randint(0, WIDTH - 20), random.randint(0, HEIGHT - 20))
        food_timer = time.time()
        GREEN_SQUARE_DURATION += 0.5

    # Add a new green circle every 2 frames
    if frame_counter % 75 == 0:
        green_squares.append(snake[0].copy())
        green_square_timers.append(time.time())

    frame_counter += 1

    # Check for collision between snake's head and green circles
    head_collided = False
    for circle, circle_timer in zip(green_squares, green_square_timers):
        if time.time() - circle_timer >= 0.25 and snake[0].distance_to(circle) < 10:
            head_collided = True
            break

    if head_collided:
        pygame.quit()
        sys.exit()

    # Draw everything
    screen.fill(WHITE)

    # Draw the indicator for the center of the screen
    pygame.draw.circle(screen, indicator_color, (WIDTH // 2, HEIGHT // 2), indicator_radius)

    # Draw the snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment.x, segment.y, 20, 20))

    # Draw and remove green circles
    for circle, circle_timer in zip(green_squares, green_square_timers):
        if time.time() - circle_timer < GREEN_SQUARE_DURATION:
            pygame.draw.circle(screen, GREEN, (int(circle.x) + 10, int(circle.y) + 10), 10)  # 10 is the radius of the circle
        else:
            green_squares.remove(circle)
            green_square_timers.remove(circle_timer)

    # Draw food
    pygame.draw.rect(screen, FOOD_COLOR, (food_position.x, food_position.y, 20, 20))

    pygame.display.flip()

    if frame_counter >= 75:
        frame_counter = 0
