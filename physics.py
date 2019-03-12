import json
import sys
from pyfrc.physics import drivetrains


class PhysicsEngine:
    def __init__(self, physics_controller):
        """
        :param physics_controller: `pyfrc.physics.core.Physics` object
                                   to communicate simulation effects to
        """
        self.physics_controller = physics_controller
        # Load ports
        with open(sys.path[0] + "/ports.json") as f:
            self.ports = json.load(f)

    def update_sim(self, hal_data, now, tm_diff):
        """
        Called when the simulation parameters for the program need to be
        updated.

        :param now: The current time as a float
        :param tm_diff: The amount of time that has passed since the last
                        time that this function was called
        """
        # Simulate the drivetrain
        fl_motor = hal_data["pwm"][self.ports["drive"]["front_left"]]["value"]
        fr_motor = hal_data["pwm"][self.ports["drive"]["front_right"]]["value"]

        speed, rotation_speed = drivetrains.TwoMotorDrivetrain().get_vector(
            -fl_motor, fr_motor)
        self.physics_controller.drive(speed, rotation_speed, tm_diff)
