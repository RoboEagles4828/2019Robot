import sys
import os
import json
import wpilib

from digital_input import DigitalInput


class Dumper:

    dumper_solenoid: wpilib.DoubleSolenoid
    dumper_extender: wpilib.DoubleSolenoid
    dumper_servo_0: wpilib.Servo
    dumper_servo_1: wpilib.Servo
    dumper_prox: DigitalInput

    def __init__(self):
        with open(sys.path[0] +
                  ("/../" if os.getcwd()[-5:-1] == "test" else "/") +
                  "config/dumper.json") as f:
            self.config = json.load(f)
        self.pos = False
        self.extender_pos = False
        self.servo_timer = wpilib.Timer()
        self.servo_timer_started = False

    def set(self, pos):
        self.pos = pos

    def setExtender(self, pos):
        self.extender_pos = pos

    def getProx(self):
        return self.dumper_prox.get()

    def execute(self):
        # Set servos
        if self.getProx() and not self.pos:
            self.dumper_servo_0.set(self.config["servo"]["pos_0_out"])
            self.dumper_servo_1.set(self.config["servo"]["pos_1_out"])
        else:
            self.dumper_servo_0.set(self.config["servo"]["pos_0_in"])
            self.dumper_servo_1.set(self.config["servo"]["pos_1_in"])
        # Set solenoid based on set position and servo timer
        if self.pos:
            if not self.servo_timer_started:
                self.servo_timer.start()
                self.servo_timer_started = True
            elif self.servo_timer.hasPeriodPassed(self.config["servo_delay"]):
                self.dumper_solenoid.set(wpilib.DoubleSolenoid.Value.kForward)
        else:
            self.servo_timer.reset()
            self.servo_timer_started = False
            self.dumper_solenoid.set(wpilib.DoubleSolenoid.Value.kReverse)
        # Set extender
        self.dumper_extender.set(
            wpilib.DoubleSolenoid.Value.kForward if self.
            extender_pos else wpilib.DoubleSolenoid.Value.kReverse)
