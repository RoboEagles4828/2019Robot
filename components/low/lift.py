import wpilib
import ctre

class Lift:
    lift_front: ctre.WPI_TalonSRX
    lift_back: ctre.WPI_TalonSRX
    lift_drive_front: wpilib.Victor
    lift_drive_back: wpilib.Victor
    lift_top_limit_front: wpilib.DigitalInput
    lift_top_limit_back: wpilib.DigitalInput
    lift_bot_limit_front: wpilib.DigitalInput
    lift_bot_limit_back: wpilib.DigitalInput
    lift_prox_front: wpilib.DigitalInput
    lift_prox_back: wpilib.DigitalInput

    def __init__(self):
        self.finished = True
        self.front_speed = 0
        self.back_speed = 0
        self.front_drive_speed = 0
        self.back_drive_speed = 0

    def driveFront(self, speed):
        self.front_speed = speed

    def driveBack(self, speed):
        self.back_speed = speed

    def liftUp(self, speed):
        self.finished = True
        self.frontUp(speed)
        self.backUp(speed)

    def liftDown(self, speed):
        self.finished = True
        self.frontDown(speed)
        self.backDown(speed)

    def backUp(self, speed):
        if not self.lift_top_limit_back.get():
            self.back_speed = speed
            self.finished = False

    def backDown(self, speed):
        if not self.lift_bot_limit_back.get():
            self.back_speed = -speed
            self.finished = False

    def frontUp(self, speed):
        if not self.lift_top_limit_front.get():
            self.front_speed = speed
            self.finished = False
    
    def frontDown(self, speed):
        if not self.lift_bot_limit_front.get():
            self.front_speed = -speed
            self.finished = False

    def getProxFront(self):
        return self.lift_prox_front.get()

    def getProxBack(self):
        return self.lift_prox_back.get()

    def execute(self):
        self.lift_front.set(self.front_speed)
        self.lift_back.set(self.back_speed)
        self.lift_drive_front.set(self.front_drive_speed)
        self.lift_drive_back.set(self.back_drive_speed)