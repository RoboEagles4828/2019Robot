import json
import sys
import os
import logging

from components.low.arm import Arm
from components.motionprofiling.curve import Curve

class ArmMover:

    arm: Arm

    def __init__(self, pos="hatch_in"):
        with open(sys.path[0] + ("/../" if os.getcwd()[-5:-1] == "test" else "/") + "arm.json") as f:
            self.config = json.load(f)
        self.logger = logging.getLogger("ArmMover")
        self.arm_curve = Curve(self.config["arm"]["set"][pos], self.config["arm"]["set"][pos],
                               min_speed=self.config["arm"]["min_speed"],
                               max_speed=self.config["arm"]["max_speed"],
                               max_acc=self.config["arm"]["max_acc"],
                               reverse=False
                               )
        self.wrist_curve = Curve(self.config["wrist"]["set"][pos], self.config["wrist"]["set"][pos],
                                 min_speed=self.config["wrist"]["min_speed"],
                                 max_speed=self.config["wrist"]["max_speed"],
                                 max_acc=self.config["wrist"]["max_acc"],
                                 reverse=False
                                 )
        self.arm_enabled = False
        self.wrist_enabled = False
        self.pos = pos
        self.arm_err_total = 0
        self.arm_speed = 0
        self.arm_pos = 0
        self.arm_pos_speed = 0
        self.arm_base_speed = 0
        self.arm_err = 0
        self.wrist_err_total = 0
        self.wrist_speed = 0
        self.wrist_pos = 0
        self.wrist_pos_speed = 0
        self.wrist_base_speed = 0
        self.wrist_err = 0

    def set(self, pos):
        if self.pos != pos:
            # Set arm curve
            self.arm_curve.setStart(self.arm.getArmEnc())
            self.arm_curve.setEnd(self.config["arm"]["set"][pos])
            self.arm_enabled = True
            # Set wrist curve
            self.wrist_curve.setStart(self.arm.getWristEnc())
            self.wrist_curve.setEnd(self.config["wrist"]["set"][pos])
            self.wrist_enabled = True
            # Set position
            self.pos = pos

    def disableArm(self):
        self.arm_err_total = 0
        self.arm_speed = 0
        self.arm_enabled = False

    def disableWrist(self):
        self.wrist_err_total = 0
        self.wrist_speed = 0
        self.wrist_enabled = False

    def disable(self):
        self.disableArm()
        self.disableWrist()

    def isEnabled(self):
        return self.arm_enabled or self.wrist_enabled

    def debug(self):
        logging.info("\n       |  Ctl  |  Pos  |  Set  |  Spd  |  Err  |  Crv  |  Out  |\
                      \nArm    | %5.0d | %5.0d | %5.0d | %5.2f | %5.2f | %5.2f | %5.2f |\
                      \nWrist  | %5.0d | %5.0d | %5.0d | %5.2f | %5.2f | %5.2f | %5.2f |",
                     self.arm_enabled, self.arm_pos, self.config["arm"]["set"][self.pos], self.arm_pos_speed, self.arm_err, self.arm_base_speed, self.arm_speed,
                     self.wrist_enabled, self.wrist_pos, self.config["wrist"]["set"][self.pos], self.wrist_pos_speed, self.wrist_err, self.wrist_base_speed, self.wrist_speed
                     )

    def execute(self):
        # Get arm position and position speed
        arm_pos = self.arm.getArmEnc()
        arm_pos_speed = arm_pos - self.arm_pos
        # Get arm base speed
        arm_base_speed = self.arm_curve.getSpeed(arm_pos)
        # Calculate arm error
        arm_err = self.arm_base_speed * self.config["arm"]["max_pos_speed"] - arm_pos_speed
        if self.arm_enabled:
            # Add arm error to total
            self.arm_err_total += arm_err
            # Add arm base speed change and PID to arm speed
            self.arm_speed += arm_base_speed - self.arm_base_speed + \
                              self.config["arm"]["p"] / self.config["arm"]["max_pos_speed"] * arm_err + \
                              self.config["arm"]["i"] / self.config["arm"]["max_pos_speed"] * self.arm_err_total + \
                              self.config["arm"]["d"] / self.config["arm"]["max_pos_speed"] * (arm_err - self.arm_err)
            if abs(self.arm_speed) > 1:
                self.arm_speed /= abs(self.arm_speed)
            # Disable arm if stopped
            if arm_base_speed == 0:
                self.disableArm()
        # Set arm speed
        self.arm.setArmSpeed(self.arm_speed)
        # Set old variables
        self.arm_pos = arm_pos
        self.arm_pos_speed = arm_pos_speed
        self.arm_base_speed = arm_base_speed
        self.arm_err = arm_err
        # Get wrist position and position speed
        wrist_pos = self.arm.getWristEnc()
        wrist_pos_speed = wrist_pos - self.wrist_pos
        # Get wrist base speed
        wrist_base_speed = self.wrist_curve.getSpeed(wrist_pos)
        # Calculate wrist error
        wrist_err = self.wrist_base_speed * self.config["wrist"]["max_pos_speed"] - wrist_pos_speed
        if self.wrist_enabled:
            # Add wrist error to total
            self.wrist_err_total += wrist_err
            # Add wrist base speed change and PID to wrist speed
            self.wrist_speed += wrist_base_speed - self.wrist_base_speed + \
                              self.config["wrist"]["p"] / self.config["wrist"]["max_pos_speed"] * wrist_err + \
                              self.config["wrist"]["i"] / self.config["wrist"]["max_pos_speed"] * self.wrist_err_total + \
                              self.config["wrist"]["d"] / self.config["wrist"]["max_pos_speed"] * (wrist_err - self.wrist_err)
            if abs(self.wrist_speed) > 1:
                self.wrist_speed /= abs(self.wrist_speed)
            # Disable wrist if stopped
            if wrist_base_speed == 0:
                self.disableWrist()
        # Set wrist speed
        self.arm.setWristSpeed(self.wrist_speed)
        # Set old variables
        self.wrist_pos = wrist_pos
        self.wrist_pos_speed = wrist_pos_speed
        self.wrist_base_speed = wrist_base_speed
        self.wrist_err = wrist_err
