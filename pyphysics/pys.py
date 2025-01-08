import math
import re
from colorama import Fore
import json

with open("pyphysics/settings.json", "r") as f:
    settings = json.load(f)
SCALE = settings["Visualization"]["SCALE"]

class options:

    WIDTH = settings["Visualization"]["WIDTH"]
    HEIGHT = settings["Visualization"]["HEIGHT"]
    WINDOW_NAME = settings["Visualization"]["WINDOW_NAME"]
    SCREEN_TEARING = settings["Visualization"]["SCREEN_TEARING"]
    BODY_RADIUS = settings["Visualization"]["BODY_RADIUS"]
    SHOW_PATHS = settings["Visualization"]["SHOW_PATHS"]
    PATH_THICKNESS = settings["Visualization"]["PATH_THICKNESS"]
    PATH_COLOR = tuple(settings["Visualization"]["PATH_COLOR"])

    G_CONST = settings["Physics"]["G_CONST"]
    SOFTENING = settings["Physics"]["SOFTENING"]
    MAX_SIM_UPDATE_SPEED = settings["Physics"]["MAX_SIM_UPDATE_SPEED"]
    BODY_1_MASS = settings["Physics"]["BODY_1_MASS"]
    BODY_2_MASS = settings["Physics"]["BODY_2_MASS"]

    BACKGROUND_COLOR = tuple(settings["Color_Scheme"]["BACKGROUND_COLOR"])
    BODY_COLORS = [tuple(color) for color in settings["Color_Scheme"]["BODY_COLORS"]]

    STEPS_PER_FRAME = settings["Performance"]["STEPS_PER_FRAME"]
    MAX_ALLOWED_FPS = settings["Performance"]["MAX_ALLOWED_FPS"]
    DELTA_TIME = settings["Performance"]["DELTA_TIME"]


class Vector2(object):
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def length(self):
        return math.sqrt(self.lengthSq())

    def lengthSq(self):
        return self.x ** 2 + self.y ** 2

    def subtract(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def normalize(self):
        length = self.length()
        if length == 0:
            return Vector2(0, 0)
        return Vector2(self.x / length, self.y / length)

    def add(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def SCALE(self, factor):
        return Vector2(self.x * factor, self.y * factor)

class Body(object):
    def __init__(self, mass, init_position, init_velocity):
        self.mass = mass
        self.position = init_position
        self.velocity = init_velocity
        self.path = []

    def update(self, participants, delta_t):
        gravity_x = 0.0
        gravity_y = 0.0

        for peer in participants:
            if peer == self:
                continue

            relative_pos = peer.position.subtract(self.position)
            distance_sq = relative_pos.lengthSq()

            distance_sq += options.SOFTENING

            acceleration = (options.G_CONST * peer.mass) / distance_sq
            direction = relative_pos.normalize()
            gravity_x += acceleration * direction.x
            gravity_y += acceleration * direction.y

        self.velocity = self.velocity.add(Vector2(gravity_x, gravity_y).SCALE(delta_t))
        self.position = self.position.add(self.velocity.SCALE(delta_t))

        self.path.append(self.position)

participants = [
    Body(options.BODY_1_MASS, Vector2(-50, 0), Vector2(0, 1)),
    Body(options.BODY_2_MASS, Vector2(50, 0), Vector2(0, -1)),
]

def extract_number(text):
    match = re.search(r'-?\d+', text)
    if match:
        return int(match.group())
    return None

max_speed = extract_number(options.MAX_SIM_UPDATE_SPEED)
if max_speed is not None:
    if max_speed > options.MAX_ALLOWED_FPS:
        print(Fore.LIGHTRED_EX + f"WARN: Requested FPS ({max_speed}) exceeds maximum allowed ({options.MAX_ALLOWED_FPS}). Capping at {options.MAX_ALLOWED_FPS}.")
        max_speed = options.MAX_ALLOWED_FPS
    elif max_speed < 0:
        print(Fore.RED + "Provide a positive max sim speed")
        quit(1)
    elif max_speed == options.MAX_ALLOWED_FPS:
        print(Fore.LIGHTRED_EX + f"WARN: Max sim speed is the same as the max sim speed cap. Errors may arise")
        print(Fore.LIGHTYELLOW_EX + f"Running {options.WINDOW_NAME} at {max_speed} frames per second")
    elif max_speed == 0:
        print(Fore.RED + "Provide a max sim speed greater than 0")
        quit(1)
    else:
        print(Fore.GREEN + f"Running {options.WINDOW_NAME} at {max_speed} frames per second")
else:
    print(Fore.RED + "Provide a max sim speed")
    quit(1)