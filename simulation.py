import pygame
import random
import math
from radar import Radar

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

# Generate random targets
def generate_random_targets(num_targets=10):
    targets = []
    for _ in range(num_targets):
        position = (random.randint(100, 700), random.randint(100, 700))
        speed = 0.1
        heading = random.uniform(0, 360)
        targets.append({'position': list(position), 'rcs': random.uniform(1, 10), 'speed': speed, 'heading': heading})
    return targets

# Initialize targets
targets = generate_random_targets()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update target positions
    for target in targets:
        speed = target['speed']
        heading = target['heading']
        dx = speed * math.cos(math.radians(heading))
        dy = speed * math.sin(math.radians(heading))
        # Update position while keeping it within bounds
        target['position'][0] = min(max(target['position'][0] + dx, 0), WIDTH)
        target['position'][1] = min(max(target['position'][1] + dy, 0), HEIGHT)

    # Update radar sweep angle
    radar.update_sweep()

    # Detect targets by simulating collision
    radar.detect_collision(targets)

    # Draw radar and sweep
    radar.draw_radar(screen)
    radar.draw_sweep(screen)

    # Draw persistent blips from previous sweeps
    radar.draw_blips(screen)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()
