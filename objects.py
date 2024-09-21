import random
import math

# Scaling factors
KM_PER_PIXEL = 1  # 1 km = 1 pixel
SPEED_SCALING_FACTOR = 1 / 60  # 1 km/h = 1/60 pixels/frame at 60 FPS

class Aircraft:
    def __init__(self, speed_kmph=129, heading=45, rcs=10):
        """ Initialize an Aircraft object with speed, heading, and RCS """
        self.x = random.randint(100, 700)
        self.y = random.randint(100, 700)
        self.speed = speed_kmph * SPEED_SCALING_FACTOR  # Speed in pixels/frame
        self.heading = heading
        self.rcs = rcs  # Radar Cross Section in m²
        self.illuminated = False  # Track if the target is illuminated

    def move(self):
        """ Moves the aircraft based on speed and heading """
        radian_heading = math.radians(self.heading)
        self.x += self.speed * math.cos(radian_heading)
        self.y += self.speed * math.sin(radian_heading)

    def get_position(self):
        """ Returns the current position of the aircraft """
        return (int(self.x), int(self.y))

class Ship:
    def __init__(self, speed_kmph=5.14, heading=90, rcs=100):
        """ Initialize a Ship object with speed, heading, and RCS """
        self.x = random.randint(100, 700)
        self.y = random.randint(100, 700)
        self.speed = speed_kmph * SPEED_SCALING_FACTOR  # Speed in pixels/frame
        self.heading = heading
        self.rcs = rcs  # Radar Cross Section in m²
        self.illuminated = False  # Track if the target is illuminated

    def move(self):
        """ Moves the ship based on speed and heading """
        radian_heading = math.radians(self.heading)
        self.x += self.speed * math.cos(radian_heading)
        self.y += self.speed * math.sin(radian_heading)

    def get_position(self):
        """ Returns the current position of the ship """
        return (int(self.x), int(self.y))
