import sys
import os
import json
import wpilib


class Dumper:
    dumper_servo: wpilib.Servo
    dumper_topservo : wpilib.Servo
    dumper_prox: wpilib.DigitalInput
    dumper_sol: wpilib.DoubleSolenoid

    def __init__(self):
        with open(sys.path[0] +
                  ("/../" if os.getcwd()[-5:-1] == "test" else "/") +
                  "config/dumper.json") as f:
            self.config = json.load(f)
        self.pos = False
        self.servo_timer = wpilib.Timer()
        self.waiting = False

    def set(self, pos):
        self.pos = pos

    def execute(self):
        if self.dumper_prox.get() and not self.pos:
            self.dumper_servo.set(self.config["servo"]["on"])
            self.dumper_topservo.set(self.config["topservo"]["on"])
        else:
            self.dumper_servo.set(self.config["servo"]["off"])
            self.dumper_topservo.set(self.config["topservo"]["off"])
        if not self.waiting and self.pos:
            self.waiting = True
            self.servo_timer.start()
        if self.waiting and self.pos and self.servo_timer.hasPeriodPassed(0.3):
            self.dumper_sol.set(wpilib.DoubleSolenoid.Value.kForward)
            self.waiting = False
        if not self.pos:
            self.dumper_sol.set(wpilib.DoubleSolenoid.Value.kReverse)
            self.servo_timer.reset()