import logging
import wpilib

from components.low.arm import Arm
from components.motionprofiling.curve import Curve

class ArmMover:

    arm: Arm

    arm_set = {
        "hatch_in": 0,
        "hatch_out_1": 520,
        "hatch_out_2": 2335,
        "ball_in": 145,
        "ball_out_1": 1200,
        "ball_out_2": 2335
    }
    wrist_set = {
        "hatch_in": 2295,
        "hatch_out_1": 2860,
        "hatch_out_2": 2205,
        "ball_in": 2080,
        "ball_out_1": 1705,
        "ball_out_2": 1770
    }
    arm_max_pos_speed = 8
    arm_min_speed = 0.1
    arm_max_speed = 0.8
    arm_max_acc = 0.03
    wrist_max_pos_speed = 8
    wrist_min_speed = 0.1
    wrist_max_speed = 0.8
    wrist_max_acc = 0.03
    arm_p = 10 / 1024
    arm_i = 0 / 1024
    arm_d = 0 / 1024
    wrist_p = 10 / 1024
    wrist_i = 0 / 1024
    wrist_d = 0 / 1024

    def __init__(self, pos="hatch_in"):
        self.logger = logging.getLogger("ArmMover")
        self.arm_curve = Curve(self.arm_set[pos], self.arm_set[pos],
                               min_speed=self.arm_min_speed,
                               max_speed=self.arm_max_speed,
                               max_acc=self.arm_max_acc,
                               reverse=False
                               )
        self.wrist_curve = Curve(self.wrist_set[pos], self.wrist_set[pos],
                                 min_speed=self.wrist_min_speed,
                                 max_speed=self.wrist_max_speed,
                                 max_acc=self.wrist_max_acc,
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
            self.arm_curve.setEnd(self.arm_set[pos])
            self.arm_enabled = True
            # Set wrist curve
            self.wrist_curve.setStart(self.arm.getWristEnc())
            self.wrist_curve.setEnd(self.wrist_set[pos])
            self.wrist_enabled = True
            # Set position
            self.pos = pos

    def disable(self):
        self.arm_enabled = False
        self.wrist_enabled = False

    def isEnabled(self):
        return self.arm_enabled or self.wrist_enabled

    def debug(self):
        logging.info("\n       |  Ctl  |  Pos  |  Set  |  Err  |  Out  |\nArm    | %5r | %5d | %5d | %5d | %5.3f |\nWrist  | %5r | %5d | %5d | %5d | %5.3f |",
                     self.arm_enabled, self.arm_pos, self.arm_set[self.pos], self.arm_err, self.arm_speed,
                     self.wrist_enabled, self.wrist_pos, self.wrist_set[self.pos], self.wrist_err, self.wrist_speed
                     )

    def execute(self):
        if self.arm_enabled:
            # Get arm position and position speed
            arm_pos = self.arm.getArmEnc()
            arm_pos_speed = arm_pos - self.arm_pos
            # Get arm base speed
            arm_base_speed = self.arm_curve.getSpeed(arm_pos)
            # Calculate arm error
            arm_err = self.arm_base_speed * self.arm_max_pos_speed - arm_pos_speed
            # Add arm error to total
            self.arm_err_total += arm_err
            # Add arm base speed change and PID to arm speed
            self.arm_speed += arm_base_speed - self.arm_base_speed + \
                              self.arm_p * arm_err + \
                              self.arm_i * self.arm_err_total + \
                              self.arm_d * (arm_err - self.arm_err)
            if abs(self.arm_speed) > 1:
                self.arm_speed /= abs(self.arm_speed)
            # Set arm speed
            self.arm.setArmSpeed(self.arm_speed)
            # Set old variables
            self.arm_pos = arm_pos
            self.arm_pos_speed = arm_pos_speed
            self.arm_base_speed = arm_base_speed
            self.arm_err = arm_err
            # Disable arm if stopped
            if arm_base_speed == 0:
                self.arm.setArmSpeed(0)
                self.arm_enabled = False
        if self.wrist_enabled:
            # Get wrist position and position speed
            wrist_pos = self.arm.getWristEnc()
            wrist_pos_speed = wrist_pos - self.wrist_pos
            # Get wrist base speed
            wrist_base_speed = self.wrist_curve.getSpeed(wrist_pos)
            # Calculate wrist error
            wrist_err = self.wrist_base_speed * self.wrist_max_pos_speed - wrist_pos_speed
            # Add wrist error to total
            self.wrist_err_total += wrist_err
            # Add wrist base speed change and PID to wrist speed
            self.wrist_speed += wrist_base_speed - self.wrist_base_speed + \
                              self.wrist_p * wrist_err + \
                              self.wrist_i * self.wrist_err_total + \
                              self.wrist_d * (wrist_err - self.wrist_err)
            if abs(self.wrist_speed) > 1:
                self.wrist_speed /= abs(self.wrist_speed)
            # Set wrist speed
            self.arm.setWristSpeed(self.wrist_speed)
            # Set old variables
            self.wrist_pos = wrist_pos
            self.wrist_pos_speed = wrist_pos_speed
            self.wrist_base_speed = wrist_base_speed
            self.wrist_err = wrist_err
            # Disable wrist if stopped
            if wrist_base_speed == 0:
                self.arm.setWristSpeed(0)
                self.wrist_enabled = False
