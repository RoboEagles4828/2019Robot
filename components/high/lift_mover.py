import json
import sys
import os

from components.low.drivetrain import DriveTrain
from components.low.lift import Lift

class LiftMover:

    drive: DriveTrain
    lift: Lift

    def __init__(self):
        with open(sys.path[0] + ("/../" if os.getcwd()[-5:-1] == "test" else "/") + "config/lift.json") as f:
            self.config = json.load(f)
        self.enabled = False
        self.status = False

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False
        self.status = False

    def execute(self):
        if self.enabled and not self.status:
            # Lift up
            if (self.lift.getFrontPos() != 1) or (self.lift.getBackPos() != 1):
                self.lift.setFrontSpeed(self.config["lift"]["speed"])
                #self.lift.setBackSpeed(self.config["lift"]["speed"] - self.config["lift"]["p"] * self.lift.getNavx())
                self.lift.setBackSpeed(self.config["lift"]["speed"] * self.config["lift"]["back_ratio"])
                return
            # Drive lift and drivetrain
            if not self.lift.getProxFront():
                self.drive.setSpeeds(self.config["drive_speed"], self.config["drive_speed"])
                self.lift.setDriveSpeed(self.config["lift"]["drive_speed"])
                return
            # Stop lift and drivetrain
            self.drive.setSpeeds(0, 0)
            self.lift.setDriveSpeed(0)
            self.status = True
        elif self.enabled and self.status:
            # Lift front up
            if self.lift.getFrontPos() != -1:
                self.lift.setFrontSpeed(-self.config["lift"]["speed"])
                return
            # Drive lift and drivetrain
            if not self.lift.getProxBack():
                self.drive.setSpeeds(self.config["drive_speed"], self.config["drive_speed"])
                self.lift.setDriveSpeed(self.config["lift"]["drive_speed"])
                return
            # Stop lift and drivetrain
            self.drive.setSpeeds(0, 0)
            self.lift.setDriveSpeed(0)
            # Lift back up
            if self.lift.getBackPos() != -1:
                self.lift.setBackSpeed(-self.config["lift"]["speed"])
                return
            self.enabled = False
            self.status = False
