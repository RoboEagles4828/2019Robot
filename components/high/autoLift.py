import wpilib

from components.low.lift import Lift
from components.low.drivetrain import DriveTrain

class AutoLift:

    lift: Lift
    drive: DriveTrain

    def __init__(self):
        self.enabled = False

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def execute(self):
        if self.enabled:
            while not self.lift.getLimitFront() or not self.lift.getLimitBack():
                self.lift.setLiftSpeed(0.5)
            # Drive lift and drivetrain
            self.lift.setLiftSpeed(0)
            while not self.lift.getProxFront():
                self.lift.setDriveSpeed(0.5)
                self.drive.setSpeeds(0.1, 0.1) #Need to calibrate
            self.drive.setSpeeds(0,0)
            self.lift.setDriveSpeed(0)
            while not self.lift.getLimitFront():
                self.lift.setFrontSpeed(-0.5)
            self.lift.setFrontSpeed(0)
            while not self.lift.getProxBack():
                self.lift.setDriveSpeed(0.5)
                self.drive.setSpeeds(0.1, 0.1) #Need to calibrate
            self.drive.setSpeeds(0,0)
            self.lift.setDriveSpeed(0)
            while not self.lift.getLimitBack():
                self.lift.setBackSpeed(-0.5)
            self.lift.setBackSpeed(0)
            self.enabled = False
