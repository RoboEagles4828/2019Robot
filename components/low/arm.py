import json
import sys
import os
import wpilib
import ctre

class Arm:

    arm_left: ctre.WPI_TalonSRX
    arm_right: ctre.WPI_TalonSRX
    wrist: ctre.WPI_VictorSPX
    intake: ctre.WPI_VictorSPX
    hatch: wpilib.DoubleSolenoid
    wrist_enc: wpilib.AnalogInput

    def __init__(self):
        with open(sys.path[0] + ("/../" if os.getcwd()[-5:-1] == "test" else "/") + "arm.json") as f:
            self.config = json.load(f)
        self.arm_speed = 0
        self.wrist_speed = 0
        self.intake_speed = 0

    def setArmSpeed(self, speed):
        self.arm_speed = speed

    def setWristSpeed(self, speed):
        self.wrist_speed = speed

    def setIntakeSpeed(self, speed):
        self.intake_speed = speed

    def setHatch(self, x):
        if x:
            self.hatch.set(wpilib.DoubleSolenoid.Value.kForward)
        else:
            self.hatch.set(wpilib.DoubleSolenoid.Value.kReverse)

    def getArmSpeed(self):
        return self.arm_speed

    def getWristSpeed(self):
        return self.wrist_speed

    def getArmEnc(self):
        return self.arm_right.getQuadraturePosition() - self.config["arm"]["enc_start"]

    def setArmEnc(self):
        self.arm_right.setQuadraturePosition(self.arm_right.getPulseWidthPosition())

    def getWristEnc(self):
        return self.wrist_enc.getValue() - self.config["wrist"]["enc_start"]

    def execute(self):
        self.arm_left.set(self.arm_speed)
        self.arm_right.set(self.arm_speed)
        self.wrist.set(self.wrist_speed)
        self.intake.set(self.intake_speed)
