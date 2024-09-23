import math
import pygame
from physics import calculateFSPL, calculateReceivedPower, calculateNoisePower, calculateSNR, calculateJammingEffect

class Radar:
    def __init__(self, center, range_radius, beamwidth, sweep_speed, pt=1.0, gain_transmit=30, gain_recieve=30, frequency=10e9, noise_figure=5):
        self.center = center
        self.range_radius = range_radius
        self.beamwidth = beamwidth
        self.sweep_speed = sweep_speed
        self.pt = pt
        self.g_transmit = 10 ** (gain_transmit / 10)
        self.g_recieve = 10 ** (gain_recieve / 10)
        self.frequency = frequency
        self.wavelength = 3e8 / self.frequency
        self.angle = 0
        self.elevation = 0
        self.trail_surface = pygame.Surface((800, 800), pygame.SRCALPHA)
        self.blips = {}
        self.swept_angles = set()
        self.noise_figure = noise_figure
        self.k = 1.38e-23  # Boltzmann constant
        self.t0 = 290  # Standard temperature in Kelvin

    def calculateResponse(self, target):
        """Calculate the received power and SNR from a target."""
        distance = math.sqrt((target['position'][0] - self.center[0])**2 + (target['position'][1] - self.center[1])**2)
        
        if distance == 0 or distance > self.range_radius:
            return 0, -float('inf')  # Return 0 power and -inf SNR for out of range targets

        path_loss = calculateFSPL(distance, self.frequency)
        received_power = calculateReceivedPower(self.pt, self.g_transmit, self.g_recieve, self.wavelength, target['rcs'], distance)
        
        # Calculate noise power
        noise_power = calculateNoisePower(self.noise_figure, self.k, self.t0, self.frequency)
        
        # Calculate SNR
        snr = calculateSNR(received_power, noise_power)
        
        # Apply jamming effect if present
        if 'jamming_power' in target:
            received_power *= calculateJammingEffect(received_power, target['jamming_power'])

        return received_power, snr

    def is_within_beam(self, target_position):
        """Check if a given position is within the current radar beam."""
        target_angle = math.degrees(math.atan2(target_position[1] - self.center[1], target_position[0] - self.center[0])) % 360
        beam_start_angle = (self.angle - self.beamwidth / 2) % 360
        beam_end_angle = (self.angle + self.beamwidth / 2) % 360

        if beam_start_angle < beam_end_angle:
            return beam_start_angle <= target_angle <= beam_end_angle
        else:
            return target_angle >= beam_start_angle or target_angle <= beam_end_angle

    def detect_and_update_targets(self, targets):
        """Detect targets within the current beam and update blips."""
        start_angle = (self.angle - self.beamwidth / 2) % 360
        end_angle = (self.angle + self.beamwidth / 2) % 360

        for angle in range(int(start_angle), int(end_angle) + 1):
            self.swept_angles.add(angle % 360)

        detected_positions = set()
        for target in targets:
            target_position = tuple(map(int, target['position']))

            if self.is_within_beam(target_position):
                power_received, snr = self.calculateResponse(target)
                if power_received > 0:
                    self.blips[target_position] = (power_received, snr)
                    detected_positions.add(target_position)

        for position in list(self.blips.keys()):
            if self.is_within_beam(position) and position not in detected_positions:
                del self.blips[position]

        if len(self.swept_angles) == 360:
            self.swept_angles.clear()

    def update_sweep(self):
        """Updates the radar sweep angle."""
        self.angle = (self.angle + self.sweep_speed) % 360

    def draw_radar(self, screen):
        """Draws the radar background with concentric circles and radial lines."""
        screen.fill((0, 0, 0))  # Black background
        
        for i in range(1, 11):  # 10 concentric circles
            pygame.draw.circle(screen, (0, 100, 0), self.center, i * (self.range_radius // 10), 1)

        for angle in range(0, 360, 15):
            radian_angle = math.radians(angle)
            end_x = self.center[0] + self.range_radius * math.cos(radian_angle)
            end_y = self.center[1] + self.range_radius * math.sin(radian_angle)
            pygame.draw.line(screen, (0, 100, 0), self.center, (end_x, end_y), 1)

            # Add degree markings
            text = pygame.font.SysFont(None, 24).render(str(angle), True, (0, 255, 0))
            text_x = self.center[0] + (self.range_radius + 20) * math.cos(radian_angle)
            text_y = self.center[1] + (self.range_radius + 20) * math.sin(radian_angle)
            screen.blit(text, (text_x - text.get_width() // 2, text_y - text.get_height() // 2))

    def draw_sweep(self, screen):
        """Draws the radar sweeping beam."""
        self.trail_surface.fill((0, 0, 0, 0))  # Transparent background

        sweep_angle_rad = math.radians(self.angle)
        start_angle_rad = math.radians(self.angle - self.beamwidth / 2)
        end_angle_rad = math.radians(self.angle + self.beamwidth / 2)

        num_segments = 50
        segment_angle = (end_angle_rad - start_angle_rad) / num_segments

        for i in range(num_segments):
            alpha_value = max(0, (i * (255 // num_segments)))

            points = [self.center]

            for j in range(2):
                angle = start_angle_rad + (i + j) * segment_angle
                x = self.center[0] + self.range_radius * math.cos(angle)
                y = self.center[1] + self.range_radius * math.sin(angle)
                points.append((x, y))

            points.append(self.center)
            pygame.draw.polygon(self.trail_surface, (0, 255, 0, alpha_value), points)

        screen.blit(self.trail_surface, (0, 0))

    def draw_blips(self, screen):
        """Draws the current blips on the screen with a halo effect."""
        for position, (power, snr) in self.blips.items():
            blip_size = max(6, min(12, int(power*1e18 / self.pt)))  # Normalize by transmit power
            blip_color = (0, 255, 0)  # Green
            
            # Draw subtle halo
            halo_size = blip_size+6  # Just slightly larger than the blip
            halo_surface = pygame.Surface((halo_size*2, halo_size*2), pygame.SRCALPHA)
            pygame.draw.circle(halo_surface, (*blip_color, 75), (halo_size, halo_size), halo_size)  # Adjust halo_alpha (75) for halo intensity
            screen.blit(halo_surface, (position[0]-halo_size, position[1]-halo_size))
            
            # Draw main blip
            pygame.draw.circle(screen, blip_color, position, blip_size)
            
            # Add text to show distance
            distance = pygame.font.SysFont(None, 24).render(str(int(math.sqrt((position[0] - self.center[0])**2 + (position[1] - self.center[1])**2))), True, (0, 255, 0))
            screen.blit(distance, (position[0], position[1] + 15))

            # Display target type
            if(blip_size > 9):
                type_of_target = pygame.font.SysFont(None, 24).render("Ship", True, (0, 255, 0))
                screen.blit(type_of_target, (position[0]+15, position[1] - 15))
            else:
                type_of_target = pygame.font.SysFont(None, 24).render("A/C", True, (0, 255, 0))
                screen.blit(type_of_target, (position[0]+15, position[1] - 15))