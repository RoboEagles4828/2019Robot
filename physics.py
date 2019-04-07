import sys
import os
import json
from pyfrc.physics import motor_cfgs, tankmodel
from pyfrc.physics.units import units


class PhysicsEngine:
    def __init__(self, physics_controller):
        """
        :param physics_controller: `pyfrc.physics.core.Physics` object
                                   to communicate simulation effects to
        """
        self.physics_controller = physics_controller
        # Load ports
        with open(sys.path[0] +
                  ("/../" if os.getcwd()[-5:-1] == "test" else "/") +
                  "config/ports.json") as f:
            self.ports = json.load(f)
        # Drivetrain
        self.drivetrain = tankmodel.TankModel.theory(
            motor_cfgs.MOTOR_CFG_CIM,
            robot_mass=90 * units.lbs,
            gearing=10.71,
            nmotors=2,
            x_wheelbase=2.0 * units.feet,
            wheel_diameter=6 * units.inch)

    def update_sim(self, hal_data, now, tm_diff):
        """
        Called when the simulation parameters for the program need to be
        updated.

        :param now: The current time as a float
        :param tm_diff: The amount of time that has passed since the last
                        time that this function was called
        """
        # Get motors
        fl_motor = hal_data["pwm"][self.ports["drive"]["front_left"]]
        fr_motor = hal_data["pwm"][self.ports["drive"]["front_right"]]
        # Simulate drivetrain
        x, y, angle = self.drivetrain.get_distance(-fl_motor["value"],
                                                   fr_motor["value"], tm_diff)
        self.physics_controller.distance_drive(x, y, angle)
