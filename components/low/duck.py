import sys
import os
import json
import wpilib


class Duck:

    duck_solenoid: wpilib.DoubleSolenoid
    duck_servo_0: wpilib.Servo
    duck_servo_1: wpilib.Servo

    def __init__(self):
        with open(sys.path[0] +
                  ("/../" if os.getcwd()[-5:-1] == "test" else "/") +
                  "config/duck.json") as f:
            self.config = json.load(f)
        self.pos = False
        self.servo_pos = False

    def set(self, pos):
        self.pos = pos

    def setServo(self, pos):
        self.servo_pos = pos

    def execute(self):
        self.duck_solenoid.set(wpilib.DoubleSolenoid.Value.kForward if self.
                               pos else wpilib.DoubleSolenoid.Value.kReverse)
        if self.servo_pos:
            self.duck_servo_0.set(self.config["servo"]["pos_0_out"])
            self.duck_servo_1.set(self.config["servo"]["pos_1_out"])
        else:
            self.duck_servo_0.set(self.config["servo"]["pos_0_in"])
            self.duck_servo_1.set(self.config["servo"]["pos_1_in"])
