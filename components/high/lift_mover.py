from components.low.drivetrain import DriveTrain
from components.low.lift import Lift

class LiftMover:

    drive: DriveTrain
    lift: Lift

    drive_speed = 0.1
    lift_drive_speed = 0.5
    lift_speed = 0.5

    def __init__(self):
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
                self.lift.setLiftSpeed(self.lift_speed)
                return
            # Drive lift and drivetrain
            if not self.lift.getProxFront():
                self.drive.setSpeeds(self.drive_speed, self.drive_speed)
                self.lift.setDriveSpeed(self.lift_drive_speed)
                return
            # Stop lift and drivetrain
            self.drive.setSpeeds(0, 0)
            self.lift.setDriveSpeed(0)
            self.status = True
        elif self.enabled and self.status:
            # Lift front up
            if self.lift.getFrontPos() != -1:
                self.lift.setFrontSpeed(-self.lift_speed)
                return
            # Drive lift and drivetrain
            if not self.lift.getProxBack():
                self.drive.setSpeeds(self.drive_speed, self.drive_speed)
                self.lift.setDriveSpeed(self.lift_drive_speed)
                return
            # Stop lift and drivetrain
            self.drive.setSpeeds(0, 0)
            self.lift.setDriveSpeed(0)
            # Lift back up
            if self.lift.getBackPos() != -1:
                self.lift.setBackSpeed(-self.lift_speed)
                return
            self.enabled = False
            self.status = False
