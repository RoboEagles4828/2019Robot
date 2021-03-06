import sys
import os
import json
import pathfinder
from pathfinder.followers import EncoderFollower

from components.low.drivetrain import Drivetrain
from components.high.pathfinder.path_generator import PathGenerator


class AutoDrive:

    drive: Drivetrain

    def __init__(self):
        with open(sys.path[0] +
                  ("/../" if os.getcwd()[-5:-1] == "test" else "/") +
                  "config/auto_drive.json") as f:
            self.config = json.load(f)
        # Set default trajectory
        self.setTrajectories(self.config["drive"]["default_name"])
        # Set trajectory position
        self.pos = 0
        # Set enabled
        self.enabled = False

    def setup(self):
        self.set(0)

    def set(self, pos):
        # Get trajectory
        self.trajectory = self.trajectories[pos]
        # Set tank modifier
        modifier = pathfinder.modifiers.TankModifier(
            self.trajectory).modify(0.5)
        # Get encoder followers
        self.left = EncoderFollower(modifier.getLeftTrajectory())
        self.right = EncoderFollower(modifier.getRightTrajectory())
        # Configure encoders
        self.left.configureEncoder(self.drive.getEncLeft(), 4096, 0.2032)
        self.right.configureEncoder(self.drive.getEncRight(), 4096, 0.2032)
        # Set PIDVA values
        self.left.configurePIDVA(self.config["drive"]["left_p"],
                                 self.config["drive"]["left_i"],
                                 self.config["drive"]["left_d"],
                                 1 / self.config["drive"]["max_velocity"], 0)
        self.right.configurePIDVA(self.config["drive"]["right_p"],
                                  self.config["drive"]["right_i"],
                                  self.config["drive"]["right_d"],
                                  1 / self.config["drive"]["max_velocity"], 0)

    def next(self):
        if (self.pos + 1) < len(self.trajectories):
            self.pos += 1
            self.set(self.pos)

    def setTrajectories(self, name):
        self.trajectories = PathGenerator.get(name)

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False
        self.drive.setSpeeds(0, 0)

    def isFinished(self):
        return self.left.isFinished() and self.right.isFinished()

    def debug(self):
        return {
            "Drive Left Speed": self.drive.getSpeeds()[0],
            "Drive Right Speed": self.drive.getSpeeds()[1],
            "Drive Encoder Left": self.drive.getEncLeft(),
            "Drive Encoder Right": self.drive.getEncRight(),
            "Drive Navx": self.drive.getNavx(),
            "Drive Enabled": self.enabled
        }

    def execute(self):
        if self.enabled:
            angle_speed = self.config[
                "navx_p"] / 180 * pathfinder.boundHalfDegrees(
                    pathfinder.r2d(self.left.getHeading()) -
                    self.drive.getNavx())
            self.drive.setSpeeds(
                self.left.calculate(self.drive.getEncLeft()) +
                (angle_speed if angle_speed < 0 else 0),
                self.right.calculate(self.drive.getEncRight()) -
                (angle_speed if angle_speed > 0 else 0))
