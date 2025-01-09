import re
from colorama import Fore
import math
from pyphysics import physics

# Physics
SOFTENING = 0.01
FORCED_SIM_SPEED = "600fps"

# Performance
STEPS_PER_FRAME = 50
MAX_ALLOWED_FPS = 1000
DELTA_TIME = 0.1

def extract_number(text):
    match = re.search(r'-?\d+', text)
    return int(match.group()) if match else None
forced_speed = extract_number(FORCED_SIM_SPEED)
if forced_speed is not None:
    if forced_speed > MAX_ALLOWED_FPS:
        print(Fore.LIGHTRED_EX + f"WARN: Requested FPS ({forced_speed}) exceeds max allowed ({MAX_ALLOWED_FPS}). Capping.")
        forced_speed = MAX_ALLOWED_FPS
    elif forced_speed <= 0:
        print(Fore.RED + "Sim speed must be greater than 0")
        quit(1)
    else:
        print(Fore.LIGHTGREEN_EX + "Thank you for using PyPhysics!")
        print(Fore.GREEN + f"Running PyPhysics at {forced_speed} FPS")
else:
    print(Fore.RED + "Provide a valid sim speed in the settings")
    quit(1)

class Vector2:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def length(self):
        return math.sqrt(self.length_sq())

    def length_sq(self):
        return self.x ** 2 + self.y ** 2

    def subtract(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def normalize(self):
        length = self.length()
        return Vector2(self.x / length, self.y / length) if length > 0 else Vector2(0, 0)

    def add(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def scale(self, factor):
        return Vector2(self.x * factor, self.y * factor)