import wpilib

from components.low.lift import Lift
from components.low.drivetrain import DriveTrain

class AutoLift:

    lift: Lift
    drive: DriveTrain

    def __init__(self, speed):
        self.speed = speed
        self.enabled = False

    def liftUp(self):
        self.lift.setLiftSpeed(self.speed)

    def liftDown(self):
        self.lift.setLiftSpeed(-self.speed)

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def execute(self):
        if self.enabled:
            # Lift up
            self.liftUp()
            if not self.lift.isFinished():
                return
            # Drive lift and drivetrain
            self.lift.drive(0.3)
            self.drive.setSpeeds(0.3, 0.3)
            if not self.lift.getProxFront():
                return
            # Lift front up
            self.lift.setFrontSpeed(-self.speed)
            if not self.lift.isFinished():
                return
            # Lift back up
            self.lift.setBackSpeed(-self.speed)
            if not self.lift.isFinished():
                return
            # Disable lift and drivetrain
            self.lift.disable()
            self.drive.setSpeeds(0, 0)
            self.enabled = False
