import pathfinder
from pathfinder.followers import EncoderFollower

from components.low.drivetrain import Drivetrain


class PathFollower:

    drive: Drivetrain

    def __init__(self, trajectory, max_velocity):
        # Set tank modifier
        modifier = pathfinder.modifiers.TankModifier(trajectory).modify(0.5)
        # Get encoder followers
        self.left = EncoderFollower(modifier.getLeftTrajectory())
        self.right = EncoderFollower(modifier.getRightTrajectory())
        # Configure encoders
        self.left.configureEncoder(0, 4096, 0.2032)
        self.right.configureEncoder(0, 4096, 0.2032)
        # Set PIDVA values
        self.left.configurePIDVA(1.0, 0.0, 0.0, 1 / max_velocity, 0)
        self.right.configurePIDVA(1.0, 0.0, 0.0, 1 / max_velocity, 0)
        # Set enabled
        self.enabled = False

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def execute(self):
        if self.enabled:
            self.drive.setSpeeds(
                self.left.calculate(self.drive.getEncLeft()),
                self.right.calculate(self.drive.getEncRight()))
