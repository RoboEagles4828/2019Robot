import sys
import os
import json

from components.low.drivetrain import Drivetrain
from components.low.lift import Lift


class LiftMover:

    drive: Drivetrain
    lift: Lift

    def __init__(self):
        with open(sys.path[0] +
                  ("/../" if os.getcwd()[-5:-1] == "test" else "/") +
                  "config/lift.json") as f:
            self.config = json.load(f)
        self.enabled = False
        self.status = False

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False
        self.status = False

    def isEnabled(self):
        return self.enabled

    def set(self, speed):
        if self.config["lift"]["use_navx"] == 1:
            if (self.lift.getNavx() < 0) != (speed > 0):
                self.lift.setFrontSpeed(speed)
                self.lift.setBackSpeed(
                    speed - self.config["lift"]["p"] * self.lift.getNavx())
            else:
                self.lift.setFrontSpeed(
                    speed + self.config["lift"]["p"] * self.lift.getNavx())
                self.lift.setBackSpeed(speed)
        else:
            if speed > 0:
                self.lift.setFrontSpeed(speed)
                self.lift.setBackSpeed(self.config["lift"]["up_ratio"] * speed)
            else:
                self.lift.setFrontSpeed(
                    self.config["lift"]["down_ratio"] * speed)
                self.lift.setBackSpeed(speed)

    def debug(self):
        return {
            "Lift Drive Speed": self.lift.getDriveSpeed(),
            "Lift Front Speed": self.lift.getFrontSpeed(),
            "Lift Back Speed": self.lift.getBackSpeed(),
            "Lift Prox Front": self.lift.getProxFront(),
            "Lift Prox Back": self.lift.getProxBack(),
            "Lift Limit Front": self.lift.getLimitFront(),
            "Lift Limit Back": self.lift.getLimitBack(),
            "Lift Front Position": self.lift.getFrontPos(),
            "Lift Back Position": self.lift.getBackPos(),
            "Lift Navx": self.lift.getNavx(),
            "Lift Enabled": self.enabled,
            "Lift Status": self.status
        }

    def execute(self):
        if self.enabled and not self.status:
            # Lift up
            if (self.lift.getFrontPos() != 1) or (self.lift.getBackPos() != 1):
                self.set(self.config["lift"]["speed"])
                return
            # Drive lift and drivetrain
            if not self.lift.getProxFront():
                self.drive.setSpeeds(self.config["drive_speed"],
                                     self.config["drive_speed"])
                self.lift.setDriveSpeed(self.config["lift"]["drive_speed"])
                return
            # Stop lift drive and drivetrain
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
                self.drive.setSpeeds(self.config["drive_speed"],
                                     self.config["drive_speed"])
                self.lift.setDriveSpeed(self.config["lift"]["drive_speed"])
                return
            # Stop drive
            self.lift.setDriveSpeed(0)
            self.drive.setSpeeds(0, 0)
            # Lift back up
            if self.lift.getBackPos() != -1:
                self.lift.setBackSpeed(-self.config["lift"]["speed"])
                return
            self.enabled = False
            self.status = False
        else:
            self.lift.disable()
