# 🕹️ Pygame Crash Course
# A beginner-friendly introduction to building games using Pygame!

# 📌 Make sure you have pygame installed:
# !pip install pygame
python
Copy
Edit
## 🧱 Step 1: Basic Pygame Setup

import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Crash Course")

# Set up colors
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)

# Game clock
clock = pygame.time.Clock()

# Main loop (press the X button to close the window)
running = True
while running:
    screen.fill(WHITE)  # Clear the screen with white
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Draw a simple rectangle
    pygame.draw.rect(screen, BLUE, (100, 100, 150, 80))
    
    pygame.display.flip()  # Update the screen
    clock.tick(60)  # Limit FPS to 60

pygame.quit()
python
Copy
Edit
## 🎮 Step 2: Moving Objects with Arrow Keys

# Let's move a square using keyboard input!

import pygame
pygame.init()

WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Keyboard Input Example")

clock = pygame.time.Clock()
WHITE = (255, 255, 255)
RED = (255, 0, 0)

x, y = 300, 220
speed = 5

running = True
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: x -= speed
    if keys[pygame.K_RIGHT]: x += speed
    if keys[pygame.K_UP]: y -= speed
    if keys[pygame.K_DOWN]: y += speed

    pygame.draw.rect(screen, RED, (x, y, 50, 50))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
python
Copy
Edit
## ⚽ Step 3: Bouncing Ball with Simple Physics

import pygame
pygame.init()

WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball")

clock = pygame.time.Clock()
WHITE = (255, 255, 255)
BALL_COLOR = (0, 200, 200)

ball_x, ball_y = 100, 100
ball_radius = 20
ball_speed_x = 4
ball_speed_y = 3

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Ball movement
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Collision with walls
    if ball_x <= 0 or ball_x >= WIDTH - ball_radius:
        ball_speed_x *= -1
    if ball_y <= 0 or ball_y >= HEIGHT - ball_radius:
        ball_speed_y *= -1

    pygame.draw.circle(screen, BALL_COLOR, (ball_x, ball_y), ball_radius)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
python
Copy
Edit
## 🧼 Step 4: Cleanup and Summary

print("✅ You’ve completed the Pygame crash course!")
print("""
Key concepts you've practiced:
- Initializing Pygame and creating a window
- Handling input with events and key states
- Drawing shapes and updating the screen
- Basic physics with position and speed
- Collision with walls

From here, you can build:
- Pong
- Breakout
- Platformers
- Top-down shooters

Check out pygame.org/docs for more!
""")
