import logging
import wpilib
import ctre
import navx

class Lift:

    navx: navx.AHRS
    lift_front: ctre.WPI_TalonSRX
    lift_back: ctre.WPI_TalonSRX
    lift_drive_left: ctre.WPI_VictorSPX
    lift_drive_right: ctre.WPI_VictorSPX
    lift_top_limit_front: wpilib.DigitalInput
    lift_top_limit_back: wpilib.DigitalInput
    lift_bot_limit_front: wpilib.DigitalInput
    lift_bot_limit_back: wpilib.DigitalInput
    lift_prox_front: wpilib.DigitalInput
    lift_prox_back: wpilib.DigitalInput

    def __init__(self):
        self.logger = logging.getLogger("Lift")
        self.front_speed = 0
        self.back_speed = 0
        self.drive_speed = 0

    def disable(self):
        self.front_speed = 0
        self.back_speed = 0
        self.drive_speed = 0

    def drive(self, speed):
        self.drive_speed = speed

    def liftUp(self, speed):
        self.front_speed = speed
        #self.back_speed = max(speed / 2 - max(self.navx.getPitch() / 2, 0), 0)
        self.back_speed = speed / 2

    def liftDown(self, speed):
        self.front_speed = -speed
        self.back_speed = -speed / 2

    def getProxFront(self):
        return not self.lift_prox_front.get()

    def getProxBack(self):
        return not self.lift_prox_back.get()

    def isFinished(self):
        return self.getProxFront() and self.getProxBack()

    def debugNavx(self):
        return self.navx.getPitch()

    def execute(self):
        self.lift_front.set(-self.front_speed if not self.getProxFront() else 0)
        self.lift_back.set(-self.back_speed if not self.getProxBack() else 0)
        self.lift_drive_left.set(self.drive_speed)
        self.lift_drive_right.set(self.drive_speed)
