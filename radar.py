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
        
        # Dictionary to store current blips
        self.blips = {}
        # Set to keep track of angles that have been swept in the current cycle
        self.swept_angles = set()

    def calculate_response(self, target_position, rcs):
        """Calculate the received power from a target."""
        distance = math.sqrt((target_position[0] - self.center[0]) ** 2 + (target_position[1] - self.center[1]) ** 2)
        
        if distance == 0 or distance > self.range_radius:
            return 0, 0

        power_received = (self.pt * self.g**2 * (self.wavelength**2) * rcs) / ((4 * math.pi)**3 * (distance**4))
        return power_received, distance

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
        """Detect targets within the current beam and update blips immediately."""
        # Determine the range of angles covered by this sweep
        start_angle = (self.angle - self.beamwidth / 2) % 360
        end_angle = (self.angle + self.beamwidth / 2) % 360

        # Add these angles to the swept angles set
        for angle in range(int(start_angle), int(end_angle) + 1):
            self.swept_angles.add(angle % 360)

        # Check for targets within the beam
        detected_positions = set()
        for target in targets:
            target_position = tuple(map(int, target['position']))
            rcs = target['rcs']

            if self.is_within_beam(target_position):
                power_received, _ = self.calculate_response(target_position, rcs)
                if power_received > 0:
                    self.blips[target_position] = rcs
                    detected_positions.add(target_position)

        # Remove blips that are within the current sweep but not detected
        for position in list(self.blips.keys()):
            blip_angle = math.degrees(math.atan2(position[1] - self.center[1], position[0] - self.center[0])) % 360
            if self.is_within_beam(position) and position not in detected_positions:
                del self.blips[position]

        # Check if a full sweep has been completed
        if len(self.swept_angles) == 360:
            self.swept_angles.clear()  # Reset for the next sweep

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
        """Draws the current blips on the screen."""
        for position, rcs in self.blips.items():
            # Normalize RCS for blip size (adjust as needed)
            blip_size = max(3, min(10, int(rcs)))
            pygame.draw.circle(screen, (255, 255, 0), position, blip_size)