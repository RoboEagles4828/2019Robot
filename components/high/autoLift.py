import wpilib

from components.low.lift import Lift
from components.low.drivetrain import DriveTrain

class AutoLift:
    lift: Lift
    drive: DriveTrain

    def goUp(self):
        self.lift.liftUp()
    
    def goDown(self):
        self.lift.liftDown()
    
    def climb(self):
        while True:
            self.lift.liftUp()
            if self.lift.finish():
                break
        self.lift.stop()
        while not self.lift.getProxFront():
            self.lift.drive(.3)
            self.drive.setSpeeds(.3, .3)
        self.lift.stop()
        while True:
            self.lift.frontUp()
            if self.lift.finish():
                break
        while not self.lift.getProxBack():
            self.lift.drive(.3)
            self.drive.setSpeeds(.3, .3)
        self.lift.stop()
        while True:
            self.lift.backUp()
            if self.lift.finish():
                break