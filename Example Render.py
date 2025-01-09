import pygame
import pyphysics

pygame.init()
logo = pygame.image.load('logo.png')
screen = pygame.display.set_mode((800, 800), pygame.RESIZABLE, pygame.NOFRAME)
pygame.display.set_caption("Two-Body Orbit Simulation")
pygame.display.set_icon(logo)

OFFSET_X = 800 // 2
OFFSET_Y = 800 // 2
scale = 0.1

def to_screen_coords(pos):
    return int(pos.x * scale + OFFSET_X), int(-pos.y * scale + OFFSET_Y)

running = True
clock = pygame.time.Clock()

universe = pyphysics.physics.Environment(2000)

universe.add_body(pyphysics.physics.Body(100, pyphysics.Vector2(100, 0), pyphysics.Vector2(0, 20)))
universe.add_body(pyphysics.physics.Body(100, pyphysics.Vector2(-100, 0), pyphysics.Vector2(0, -20)))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    delta_time = clock.tick(pyphysics.forced_speed) / 1000.0

    # Update simulation
    for _ in range(pyphysics.STEPS_PER_FRAME):
        universe.update(delta_time)

    # Clear screen
    screen.fill((0, 0, 0))

    # Draw paths
    for p in universe.participants:
        if len(p.path) > 1:
            for i in range(1, len(p.path)):
                start = to_screen_coords(p.path[i - 1])
                end = to_screen_coords(p.path[i])
                pygame.draw.line(screen, (20, 20, 20), start, end, max(1, int(2 * scale)))

    # Draw bodies
    for p in universe.participants:
        current_pos = to_screen_coords(p.position)
        body_size = max(1, (0.05 * p.mass) * scale)
        color = p.color
        pygame.draw.circle(screen, color, current_pos, int(body_size))

    pygame.display.flip()

pygame.quit()
