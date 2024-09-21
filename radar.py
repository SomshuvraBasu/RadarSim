import math
import pygame

class Radar:
    def __init__(self, center, range_radius, beamwidth, sweep_speed, pt=1.0, g=30, frequency=10e9):
        self.center = center
        self.range_radius = range_radius
        self.beamwidth = beamwidth
        self.sweep_speed = sweep_speed
        self.pt = pt
        self.g = 10 ** (g / 10)
        self.frequency = frequency
        self.wavelength = 3e8 / self.frequency
        self.angle = 0
        self.trail_surface = pygame.Surface((800, 800), pygame.SRCALPHA)
        self.illuminated_targets = set()  # Keep track of illuminated target positions

    def calculate_response(self, target):
        target_pos = target.get_position()
        distance = math.sqrt((target_pos[0] - self.center[0]) ** 2 + (target_pos[1] - self.center[1]) ** 2)

        if distance == 0 or distance > self.range_radius:
            return 0, 0

        power_received = (self.pt * self.g**2 * (self.wavelength**2) * target.rcs) / ((4 * math.pi)**3 * (distance**4))
        return power_received, distance

    def is_target_within_beam(self, target):
        target_pos = target.get_position()
        target_angle = math.degrees(math.atan2(target_pos[1] - self.center[1], target_pos[0] - self.center[0])) % 360

        beam_start_angle = (self.angle - self.beamwidth / 2) % 360
        beam_end_angle = (self.angle + self.beamwidth / 2) % 360

        if beam_start_angle < beam_end_angle:
            return beam_start_angle <= target_angle <= beam_end_angle
        else:
            return target_angle >= beam_start_angle or target_angle <= beam_end_angle

    def update_illuminated_targets(self, targets):
        """ Update illuminated targets based on the current sweep. """
        # Track current positions of targets
        current_positions = {target.get_position() for target in targets}

        # Check which targets are newly illuminated
        for target in targets:
            if self.is_target_within_beam(target):
                power_received, _ = self.calculate_response(target)
                if power_received > 0:
                    self.illuminated_targets.add(target.get_position())  # Keep track of illuminated targets

        # Remove targets that are no longer within the beam
        self.illuminated_targets.intersection_update(current_positions)  # Keep only positions of currently active targets

    def draw_target_blip(self, screen, target):
        """ Draws the blip for a detected target. """
        if target.get_position() in self.illuminated_targets:
            power_received, distance = self.calculate_response(target)

            if power_received > 0:
                rcs_estimated = (power_received * ((4 * math.pi)**3 * (distance**4))) / (self.pt * self.g**2 * (self.wavelength**2))
                min_size = 5
                max_size = 50
                normalized_rcs = max(min(rcs_estimated / 100, 1), 0)
                blip_size = min_size + (max_size - min_size) * normalized_rcs

                x, y = target.get_position()
                pygame.draw.circle(screen, (0, 255, 0), (int(x), int(y)), int(blip_size))

    def update_sweep(self, targets):
        """ Updates the radar sweep angle and illuminated targets. """
        self.angle += self.sweep_speed
        if self.angle >= 360:
            self.angle = 0
        self.update_illuminated_targets(targets)  # Update illuminated targets after sweeping

    def draw_radar(self, screen):
        """ Draws the radar background with concentric circles and radial lines. """
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
        """ Draws the radar sweeping beam as a fading sector with intensity gradient. """
        self.trail_surface.fill((0, 0, 0, 0))  # Transparent background

        sweep_angle_rad = math.radians(self.angle)
        start_angle_rad = math.radians(self.angle - self.beamwidth / 2)
        end_angle_rad = math.radians(self.angle + self.beamwidth / 2)

        num_segments = 100
        segment_angle = (end_angle_rad - start_angle_rad) / num_segments

        for i in range(num_segments):
            alpha_value = max(0, 255 - (i * (255 // num_segments)))

            points = [self.center]

            for j in range(2):
                angle = start_angle_rad + (i + j) * segment_angle
                x = self.center[0] + self.range_radius * math.cos(angle)
                y = self.center[1] + self.range_radius * math.sin(angle)
                points.append((x, y))

            points.append(self.center)
            pygame.draw.polygon(self.trail_surface, (0, 255, 0, alpha_value), points)

        screen.blit(self.trail_surface, (0, 0))
