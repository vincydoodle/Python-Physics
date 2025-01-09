import time
import pyphysics

global G_const

class Environment:
    def __init__(self, G_const):
        self.G_const = G_const
        self.participants = []
        self.max_speed = float(pyphysics.forced_speed)
        self.time_accumulator = 0.0
        self.last_update_time = time.time()

    def add_body(self, body):
        self.participants.append(body)

    def update(self, delta_time):
        current_time = time.time()
        elapsed_time = current_time - self.last_update_time
        self.last_update_time = current_time

        max_frame_time = 1.0 / self.max_speed
        self.time_accumulator += elapsed_time

        while self.time_accumulator >= max_frame_time:
            for p in self.participants:
                p.update(self.participants, delta_time, self.G_const)
            self.time_accumulator -= max_frame_time


class Body:
    def __init__(self, mass, init_position, init_velocity):
        self.mass = mass
        self.position = init_position
        self.velocity = init_velocity
        self.path = []
        self.color = (255, 0, 0)

    def update(self, participants, delta_t, G_const):
        gravity = pyphysics.Vector2(0.0, 0.0)

        for peer in participants:
            if peer is self:
                continue

            relative_pos = peer.position.subtract(self.position)
            distance_sq = relative_pos.length_sq() + pyphysics.SOFTENING

            acceleration = (G_const * peer.mass) / distance_sq
            gravity = gravity.add(relative_pos.normalize().scale(acceleration))

        self.velocity = self.velocity.add(gravity.scale(delta_t))
        self.position = self.position.add(self.velocity.scale(delta_t))

        self.path.append(self.position)