import logging
import wpilib
import ctre
import navx


class Lift:

    lift_front: ctre.WPI_TalonSRX
    lift_back: ctre.WPI_TalonSRX
    lift_drive_left: ctre.WPI_VictorSPX
    lift_drive_right: ctre.WPI_VictorSPX
    lift_prox_front: wpilib.DigitalInput
    lift_prox_back: wpilib.DigitalInput
    lift_limit_front: wpilib.DigitalInput
    lift_limit_back: wpilib.DigitalInput
    navx: navx.AHRS

    def __init__(self):
        self.logger = logging.getLogger("Lift")
        self.drive_speed = 0
        self.front_speed = 0
        self.back_speed = 0
        self.front_pos = -1
        self.back_pos = -1

    def disable(self):
        self.drive_speed = 0
        self.front_speed = 0
        self.back_speed = 0

    def setDriveSpeed(self, speed):
        self.drive_speed = speed

    def setFrontSpeed(self, speed):
        self.front_speed = speed

    def setBackSpeed(self, speed):
        self.back_speed = speed

    def getDriveSpeed(self):
        return self.drive_speed

    def getFrontSpeed(self):
        return self.front_speed

    def getBackSpeed(self):
        return self.back_speed

    def getProxFront(self):
        return not self.lift_prox_front.get()

    def getProxBack(self):
        return not self.lift_prox_back.get()

    def getLimitFront(self):
        return not self.lift_limit_front.get()

    def getLimitBack(self):
        return not self.lift_limit_back.get()

    def getFrontPos(self):
        return self.front_pos

    def getBackPos(self):
        return self.back_pos

    def setFrontPos(self, pos):
        self.front_pos = pos

    def setBackPos(self, pos):
        self.back_pos = pos

    def getNavx(self):
        return self.navx.getYaw()

    def execute(self):
        # Get positions
        if self.front_pos == 0 and self.getLimitFront(
        ) and self.front_speed != 0:
            self.front_pos = self.front_speed / abs(self.front_speed)
        if self.front_pos != 0 and not self.getLimitFront():
            self.front_pos = 0
        if self.back_pos == 0 and self.getLimitBack() and self.back_speed != 0:
            self.back_pos = self.back_speed / abs(self.back_speed)
        if self.back_pos != 0 and not self.getLimitBack():
            self.back_pos = 0
        # Check positions and speeds
        if self.front_pos == 1 and self.front_speed > 0:
            self.front_speed = 0
        if self.front_pos == -1 and self.front_speed < 0:
            self.front_speed = 0
        if self.back_pos == 1 and self.back_speed > 0:
            self.back_speed = 0
        if self.back_pos == -1 and self.back_speed < 0:
            self.back_speed = 0
        # Set motors
        self.lift_front.set(self.front_speed)
        self.lift_back.set(self.back_speed)
        self.lift_drive_left.set(self.drive_speed)
        self.lift_drive_right.set(self.drive_speed)
