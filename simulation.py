import pygame
import random
from radar import Radar
from objects import Aircraft, Ship

pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Radar Simulator")

clock = pygame.time.Clock()

#define radar parameters
CENTER=(WIDTH // 2, HEIGHT // 2)
RANGE_RADIUS=300
BEAMWIDTH=45
SWEEP_SPEED=1
PT=100
GAIN_TRANSMIT=2
GAIN_RECIEVE=30
FREQUENCY=10e9
NOISE_FIGURE=5

radar = Radar(CENTER, RANGE_RADIUS, BEAMWIDTH, SWEEP_SPEED, PT, GAIN_TRANSMIT, GAIN_RECIEVE, FREQUENCY, NOISE_FIGURE)


def generate_random_targets(num_aircraft=5, num_ships=3):
    targets = []
    for _ in range(num_aircraft):
        targets.append(Aircraft())
    for _ in range(num_ships):
        targets.append(Ship())
    return targets

targets = generate_random_targets()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for target in targets:
        target.move()
        # Wrap around screen edges
        target.x %= WIDTH
        target.y %= HEIGHT

    radar.update_sweep()
    
    # Update this line to pass the correct data structure
    radar.detect_and_update_targets([{
        'position': t.get_position(),
        'rcs': t.rcs,
        'jamming_power': t.jamming_power
    } for t in targets])

    radar.draw_radar(screen)
    radar.draw_sweep(screen)
    radar.draw_blips(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()