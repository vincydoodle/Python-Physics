import math
import pygame
import re
from colorama import Fore, Back, Style

# -------------------Info-------------------
sim_speed = "60s"
caption = "Two-Body Orbit Simulation"
# ------------------------------------------

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
        if length == 0:  # Prevent division by zero
            return Vector2(0, 0)
        return Vector2(self.x / length, self.y / length)

    def add(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def scale(self, factor):
        return Vector2(self.x * factor, self.y * factor)

G_const = 2  # Adjusted for simulation scale

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

            if distance_sq == 0:  # Prevent division by zero
                continue

            acceleration = (G_const * peer.mass) / distance_sq
            direction = relative_pos.normalize()
            gravity_x += acceleration * direction.x
            gravity_y += acceleration * direction.y

        # Update position and velocity
        self.velocity = self.velocity.add(Vector2(gravity_x, gravity_y).scale(delta_t))
        self.position = self.position.add(self.velocity.scale(delta_t))

        # Store path for visualization
        self.path.append(self.position)

# Define two bodies with equal masses, opposite initial velocities, and appropriate distances
participants = [
    Body(100, Vector2(-50, 0), Vector2(0, 1)),
    Body(100, Vector2(50, 0), Vector2(0, -1)),
]

# Initialize Pygame
pygame.init()

def extract_number(text):
    # Regular expression to match a number in the text
    match = re.search(r'\d+', text)
    if match:
        return int(match.group())
    return None

number = extract_number(sim_speed)
if number is not None:
    print(Fore.GREEN + f'Running {caption} at {number} frames per second')
else:
    print(Fore.RED + 'Provide a sim speed')
    quit(1)

# Screen dimensions
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(caption)

# Colors
BLACK = (0, 0, 0)
BODY_COLORS = [(255, 0, 0), (0, 255, 0)]

# Scale and offset for visualization
SCALE = 5  # Scale simulation coordinates to pixels
OFFSET_X = WIDTH // 2
OFFSET_Y = HEIGHT // 2

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Function to convert simulation coordinates to screen coordinates
def to_screen_coords(pos):
    return int(pos.x * SCALE + OFFSET_X), int(-pos.y * SCALE + OFFSET_Y)

# Main loop
running = True
steps_per_frame = 5  # Number of simulation steps per frame
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update simulation
    for _ in range(steps_per_frame):
        for p in participants:
            p.update(participants, 0.1)  # Smaller delta_t for smooth motion

    # Clear screen
    screen.fill(BLACK)

    # Draw bodies and their paths
    for i, p in enumerate(participants):
        # Draw path
        if len(p.path) > 1:
            for j in range(1, len(p.path)):
                start = to_screen_coords(p.path[j - 1])
                end = to_screen_coords(p.path[j])

        # Draw current position of the body
        current_pos = to_screen_coords(p.position)
        pygame.draw.circle(screen, BODY_COLORS[i], current_pos, 10)

    # Update the display
    pygame.display.flip()

    # Control the speed of the simulation
    clock.tick(number)

# Quit Pygame
pygame.quit()
