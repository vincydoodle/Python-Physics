import matplotlib.pyplot as plt

print("A welcome from the Pypys Community!!! github.com/vincydoodle/Python-Physics")

class PhysicsRenderer:
    def __init__(self, G, m1, m2, d):
        """
        Initializes the physics renderer with constants and initial conditions.

        Args:
            G (float): Gravitational constant.
            m1 (float): Mass of object 1 (kg).
            m2 (float): Mass of object 2 (kg).
            d (float): Initial distance between the objects (m).
        """
        self.G = G  # Gravitational constant
        self.m1 = m1  # Mass 1
        self.m2 = m2  # Mass 2
        self.d = d  # Initial distance
        self.F = (G * m1 * m2) / d ** 2  # Initial gravitational force
        self.v1 = 0  # Initial velocity of mass 1 (m/s)
        self.v2 = 0  # Initial velocity of mass 2 (m/s)

    def move(self, time_step):
        """
        Updates the positions and velocities of the objects based on gravitational force.

        Args:
            time_step (float): Time increment for the simulation (s).

        Returns:
            tuple: Updated distance (m) and gravitational force (N).
        """
        # Calculate accelerations due to gravitational force
        a1 = -self.F / self.m1  # Acceleration of mass 1 (m/s^2)
        a2 = -self.F / self.m2  # Acceleration of mass 2 (m/s^2)

        # Update velocities
        self.v1 += a1 * time_step
        self.v2 += a2 * time_step

        # Update distance based on relative velocities
        self.d += (self.v2 - self.v1) * time_step

        # Recalculate gravitational force with updated distance
        self.F = (self.G * self.m1 * self.m2) / self.d ** 2

        return self.d, self.F


# Simulation parameters
G = 6.67430e-11  # Gravitational constant (m^3 kg^-1 s^-2)
m1 = 5.972e24  # Mass of Earth (kg)
m2 = 7.348e22  # Mass of Moon (kg)
d = 384400000  # Initial Earth-Moon distance (m)
time_step = 1  # Simulation time step (s)
simulation_steps = 10  # Number of steps in the simulation

# Initialize the physics renderer
renderer = PhysicsRenderer(G, m1, m2, d)

# Data collection for visualization
times = []
distances = []
forces = []

# Run the simulation
for t in range(1, simulation_steps + 1):
    d, F = renderer.move(time_step)
    times.append(t)
    distances.append(d)
    forces.append(F)

# Visualization
plt.figure(figsize=(12, 6))

# Distance over time
plt.subplot(1, 2, 1)
plt.plot(times, distances, label="Distance (m)", color="blue")
plt.xlabel("Time (s)")
plt.ylabel("Distance (m)")
plt.title("Distance Over Time")
plt.legend()

# Force over time
plt.subplot(1, 2, 2)
plt.plot(times, forces, label="Force (N)", color="orange")
plt.xlabel("Time (s)")
plt.ylabel("Force (N)")
plt.title("Force Over Time")
plt.legend()

# Adjust layout and display the plots
plt.tight_layout()
plt.show()
