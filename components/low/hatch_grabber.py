import wpilib

class HatchGrabber:
    servo_0: wpilib.Servo
    servo_1: wpilib.Servo

    def __init__(self):
        self.pos = 0

    def open(self):
        self.pos = 1

    def close(self):
        self.pos = 0

    def execute(self):
        self.servo_0.set(self.pos)
        self.servo_1.set(self.pos)