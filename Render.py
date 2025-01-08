import pygame
from pyphysics import pys

# Initialize pygame
pygame.init()

# Screen dimensions
screen = pygame.display.set_mode((pys.options.WIDTH, pys.options.HEIGHT))
pygame.display.set_caption(pys.options.WINDOW_NAME)

# Scale and offset for visualization
OFFSET_X = pys.options.WIDTH // 2
OFFSET_Y = pys.options.HEIGHT // 2

# Clock for controlling frame rate
clock = pygame.time.Clock()

def to_screen_coords(pos):
    return int(pos.x * pys.SCALE + OFFSET_X), int(-pos.y * pys.SCALE + OFFSET_Y)

# Main loop
running = True
STEPS_PER_FRAME = 5  # Number of simulation steps per frame
previous_time = pygame.time.get_ticks()  # Initialize previous time for delta calculation

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Calculate delta time
    current_time = pygame.time.get_ticks()
    delta_time = (current_time - previous_time) / 1000.0  # Convert to seconds
    previous_time = current_time

    # Handle screen tearing mode
    sim_speed_factor = 1 if pys.options.SCREEN_TEARING else delta_time * pys.max_speed

    # Update simulation
    for _ in range(STEPS_PER_FRAME):
        for p in pys.participants:
            p.update(pys.participants, 0.1 * sim_speed_factor)  # Adjust delta_t by sim speed factor

    # Clear screen
    screen.fill(pys.options.BACKGROUND_COLOR)

    # Draw paths (trails) first
    for i, p in enumerate(pys.participants):
        if len(p.path) > 1:
            for j in range(1, len(p.path)):
                start = to_screen_coords(p.path[j - 1])
                end = to_screen_coords(p.path[j])
                trail_thickness = max(1, int(pys.options.PATH_THICKNESS * pys.SCALE))
                pygame.draw.line(screen, pys.options.PATH_COLOR, start, end, trail_thickness)

    # Draw bodies on top of trails
    for i, p in enumerate(pys.participants):
        current_pos = to_screen_coords(p.position)
        body_size = max(1, int(pys.options.BODY_RADIUS * pys.SCALE))
        pygame.draw.circle(screen, pys.options.BODY_COLORS[i], current_pos, body_size)
    # Update the display
    pygame.display.flip()

    # Control the frame rate (only if screen tearing is off)
    if not pys.options.SCREEN_TEARING:
        clock.tick(pys.max_speed)

# Quit Pygame
pygame.quit()