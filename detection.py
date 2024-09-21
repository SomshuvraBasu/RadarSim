import pygame
import math

def detect_objects(screen, targets, radar):
    """ Detects objects and draws them based on radar response """
    for target in targets:
        # Calculate response power for the target
        power_received = radar.calculate_response(target)
        
        # Only illuminate the target if it falls within the radar sweep
        target_pos = target.get_position()
        angle_to_target = math.degrees(math.atan2(target_pos[1] - radar.center[1], target_pos[0] - radar.center[0])) % 360
        
        if (radar.angle - radar.beamwidth / 2 <= angle_to_target <= radar.angle + radar.beamwidth / 2):
            # Calculate a representative RCS based on received power, for display
            predicted_rcs = (power_received * (4 * math.pi)**3 * (target.get_distance(radar.center)**4)) / (radar.pt * radar.g**2)
            size = max(2, min(20, predicted_rcs))  # Size based on predicted RCS
            pygame.draw.circle(screen, (255, 255, 0), target_pos, size)  # Draw target as a circle
