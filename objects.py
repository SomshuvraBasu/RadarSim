import random
import math

KM_PER_PIXEL = 1
SPEED_SCALING_FACTOR = 1 / 100

class Target:
    def __init__(self, speed_kmph, heading, rcs, target_type):
        self.x = random.randint(100, 700)
        self.y = random.randint(100, 700)
        self.speed = speed_kmph * SPEED_SCALING_FACTOR
        self.heading = heading
        self.rcs = rcs
        self.type = target_type
        self.altitude = random.randint(0, 10000) if target_type == "Aircraft" else 0
        self.jamming_power = 0

    def move(self):
        radian_heading = math.radians(self.heading)
        self.x += self.speed * math.cos(radian_heading)
        self.y += self.speed * math.sin(radian_heading)

    def get_position(self):
        return (int(self.x), int(self.y))

    def apply_jamming(self, jamming_power):
        self.jamming_power = jamming_power

class Aircraft(Target):
    def __init__(self, speed_kmph=50, heading=45, rcs=10):
        super().__init__(speed_kmph, heading, rcs, "Aircraft")
        self.jamming_power = 0.5

class Ship(Target):
    def __init__(self, speed_kmph=5, heading=90, rcs=1000):
        super().__init__(speed_kmph, heading, rcs, "Ship")