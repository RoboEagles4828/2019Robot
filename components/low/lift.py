import wpilib
import ctre
import navx

class Lift:
    navx: navx.AHRS

    lift_front: ctre.WPI_TalonSRX
    lift_back: ctre.WPI_TalonSRX

    lift_drive_left: wpilib.Victor
    lift_drive_right: wpilib.Victor

    lift_top_limit_front: wpilib.DigitalInput
    lift_top_limit_back: wpilib.DigitalInput
    lift_bot_limit_front: wpilib.DigitalInput
    lift_bot_limit_back: wpilib.DigitalInput

    lift_prox_front: wpilib.DigitalInput
    lift_prox_back: wpilib.DigitalInput

    def __init__(self):
        self.finishedFront = True
        self.finishedBack = True
        self.front_speed = 0
        self.back_speed = 0
        self.drive_speed = 0

    def drive(self, speed):
        self.drive_speed = speed

    def liftUp(self, speed):
        self.frontUp(speed + (1 - speed) * (self.navx.getPitch() / 20))
        self.backUp(speed + (1 - speed) * -(self.navx.getPitch() / 20))

    def liftDown(self, speed):
        self.frontUp(speed + (1 - speed) * -(self.navx.getPitch() / 20))
        self.backUp(speed + (1 - speed) * (self.navx.getPitch() / 20))

    def backUp(self, speed):
        self.back_speed = speed

    def backDown(self, speed):
        self.back_speed = -speed

    def frontUp(self, speed):
        self.front_speed = speed
    
    def frontDown(self, speed):
        self.front_speed = -speed

    def getProxFront(self):
        return not self.lift_prox_front.get()

    def getProxBack(self):
        return not self.lift_prox_back.get()

    def finish(self):
        return self.finishedFront and self.finishedBack

    def stop(self):
        self.finished = True
        self.front_speed = 0
        self.back_speed = 0
        self.drive_speed = 0

    def execute(self):
        if not self.finishedFront:
            self.lift_front.set(self.front_speed)
        else:
            self.lift_front.set(0)
        if not self.finishedBack:
            self.lift_back.set(self.back_speed)
        else:
            self.lift_back.set(0)
        self.lift_drive_left.set(self.drive_speed)
        self.lift_drive_right.set(self.drive_speed)

        self.finishedFront = not self.lift_prox_front.get()
        self.finishedBack = not self.lift_prox_back.get()