import sys
import os
import json
import wpilib


class Sweeper:

    sweeper_servo_0: wpilib.Servo
    sweeper_servo_1: wpilib.Servo

    def __init__(self):
        with open(sys.path[0] +
                  ("/../" if os.getcwd()[-5:-1] == "test" else "/") +
                  "config/sweeper.json") as f:
            self.config = json.load(f)
        self.pos = False

    def set(self, pos):
        self.pos = pos

    def execute(self):
        # Set servos
        if self.pos:
            self.sweeper_servo_0.set(self.config["servo"]["pos_0_out"])
            self.sweeper_servo_1.set(self.config["servo"]["pos_1_out"])
        else:
            self.sweeper_servo_0.set(self.config["servo"]["pos_0_in"])
            self.sweeper_servo_1.set(self.config["servo"]["pos_1_in"])
