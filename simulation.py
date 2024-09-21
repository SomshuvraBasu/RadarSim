import pygame
from radar import Radar
from objects import Aircraft, Ship
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Radar Simulator")

# Clock to control frame rate
clock = pygame.time.Clock()

# Radar setup
radar = Radar(center=(WIDTH // 2, HEIGHT // 2), range_radius=300, beamwidth=45, sweep_speed=1, pt=1.0, g=30, frequency=10e9)

# Create initial radar targets
targets = [
    Aircraft(speed_kmph=180, heading=45, rcs=1),  # Aircraft moving at 180 km/h
    Ship(speed_kmph=10, heading=90, rcs=5),  # Stationary ship
    Ship(speed_kmph=15, heading=0, rcs=50)  # Stationary ship 2
]

# Function to add new targets randomly
def add_new_target():
    if random.random() < 0.05:  # 5% chance to add a new target each frame
        new_target = Aircraft(speed_kmph=random.randint(100, 300), heading=random.randint(0, 360), rcs=random.randint(1, 10))
        targets.append(new_target)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update radar sweep angle and illuminate targets
    radar.update_sweep(targets)

    # Move objects
    for target in targets:
        target.move()

    # Add new targets
    add_new_target()

    # Draw radar and sweep
    radar.draw_radar(screen)
    radar.draw_sweep(screen)

    # Detect and draw targets
    for target in targets:
        radar.draw_target_blip(screen, target)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()
