import logging
import json
import sys
import os
import wpilib
import ctre
import navx

class Lift:

    navx: navx.AHRS
    lift_front: ctre.WPI_TalonSRX
    lift_back: ctre.WPI_TalonSRX
    lift_drive_left: ctre.WPI_VictorSPX
    lift_drive_right: ctre.WPI_VictorSPX
    lift_prox_front: wpilib.DigitalInput
    lift_prox_back: wpilib.DigitalInput
    lift_limit_front: wpilib.DigitalInput
    lift_limit_back: wpilib.DigitalInput

    def __init__(self):
        self.logger = logging.getLogger("Lift")
        with open(sys.path[0] + ("/../" if os.getcwd()[-5:-1] == "test" else "/") + "config/lift.json") as f:
            self.config = json.load(f)
        self.drive_speed = 0
        self.front_speed = 0
        self.back_speed = 0
        self.front_pos = -1
        self.back_pos = -1
        self.navx_start = 0
        self.override = False

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

    def setLiftSpeed(self, speed):
        self.setFrontSpeed(speed)
        if speed != 0:
            self.setBackSpeed(min(speed - (speed / abs(speed)) * self.config["lift"]["p"] * self.getNavx(), 1))
        else:
            self.setBackSpeed(0)
        #self.lift.setBackSpeed(speed * self.config["lift"]["back_ratio"])

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

    def getNavx(self):
        return self.navx.getPitch() - self.navx_start

    def zeroNavx(self):
        self.navx_start = self.navx.getPitch()

    def oride(self, bl):
        self.override = bl

    def execute(self):
        # Get positions
        if not self.override:
            if self.front_pos == 0 and self.getLimitFront():
                if self.front_speed != 0:
                    self.front_pos = self.front_speed / abs(self.front_speed)
            if self.front_pos != 0 and not self.getLimitFront():
                self.front_pos = 0
            if self.back_pos == 0 and self.getLimitBack():
                if self.back_speed != 0:
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
