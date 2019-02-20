import json
import sys
import logging
import magicbot
import wpilib
import ctre
import os
import navx

from components.low.lift import Lift
from components.low.drivetrain import DriveTrain
from components.low.arm import Arm

class Robot(magicbot.MagicRobot):

    lift: Lift
    drive: DriveTrain
    arm: Arm

    def createObjects(self):
        self.logger = logging.getLogger("Robot")
        self.joystick = wpilib.Joystick(0)
        # Timer
        self.globalTimer = wpilib.Timer()
        self.globalTimer.start()
        # Load ports and buttons
        with open("../ports.json" if os.getcwd()[-5:-1] == "test" else sys.path[0] + "/ports.json") as f:
            ports = json.load(f)
        with open("../buttons.json" if os.getcwd()[-5:-1] == "test" else sys.path[0] + "/buttons.json") as f:
            self.buttons = json.load(f)
        # Drive
        self.front_left = ctre.WPI_TalonSRX(ports["drive"]["front_left"])
        self.front_right = ctre.WPI_TalonSRX(ports["drive"]["front_right"])
        self.back_left = ctre.WPI_TalonSRX(ports["drive"]["back_left"])
        self.back_right = ctre.WPI_TalonSRX(ports["drive"]["back_right"])
        # Arm
        self.arm_left = ctre.WPI_TalonSRX(ports["arm"]["arm_left"])
        self.arm_right = ctre.WPI_TalonSRX(ports["arm"]["arm_right"])
        self.wrist = ctre.WPI_VictorSPX(ports["arm"]["wrist"])
        self.wrist_enc = wpilib.AnalogInput(ports["arm"]["wrist_enc"])
        self.intake = ctre.WPI_VictorSPX(ports["arm"]["intake"])
        self.hatch = wpilib.DoubleSolenoid(ports["arm"]["hatch_in"], ports["arm"]["hatch_out"])
        # Lift
        self.navx = navx.ahrs.AHRS.create_spi()
        self.lift_front = ctre.WPI_TalonSRX(ports["lift"]["lift"]["front"])
        self.lift_back = ctre.WPI_TalonSRX(ports["lift"]["lift"]["back"])
        self.lift_drive_left = ctre.WPI_VictorSPX(ports["lift"]["drive"]["left"])
        self.lift_drive_right = ctre.WPI_VictorSPX(ports["lift"]["drive"]["right"])
        self.lift_top_limit_front = wpilib.DigitalInput(ports["lift"]["limit"]["top_front"])
        self.lift_top_limit_back = wpilib.DigitalInput(ports["lift"]["limit"]["top_back"])
        self.lift_bot_limit_front = wpilib.DigitalInput(ports["lift"]["limit"]["bot_front"])
        self.lift_bot_limit_back = wpilib.DigitalInput(ports["lift"]["limit"]["bot_back"])
        self.lift_prox_front = wpilib.DigitalInput(ports["lift"]["prox"]["front"])
        self.lift_prox_back = wpilib.DigitalInput(ports["lift"]["prox"]["back"])

    def teleopInit(self):
        print("Starting Teleop")
        self.navx.reset()

    def teleopPeriodic(self):
        # Drive
        try:
            self.drive.setSpeedsFromJoystick(self.joystick.getX(), self.joystick.getY(), self.joystick.getTwist())
        except:
            self.onException()
        # Lift
        try:
            if self.joystick.getRawButton(self.buttons["lift"]["drive"]):
                self.lift.drive(0.5)
            elif self.joystick.getRawButton(self.buttons["lift"]["up"]):
                self.lift.liftUp(1.0)
            elif self.joystick.getRawButton(self.buttons["lift"]["down"]):
                self.lift.liftDown(0.8)
            else:
                self.lift.disable()
        except:
            self.onException()
        # Arm
        try:
            if self.joystick.getRawButton(self.buttons["arm"]["arm_up"]):
                self.arm.setArmSpeed(0.3)
            elif self.joystick.getRawButton(self.buttons["arm"]["arm_down"]):
                self.arm.setArmSpeed(-0.3)
            else:
                self.arm.setArmSpeed(0)
        except:
            self.onException()
        # Wrist
        try:
            if self.joystick.getRawButton(self.buttons["arm"]["wrist_up"]):
                self.arm.setWristSpeed(-0.9)
            elif self.joystick.getRawButton(self.buttons["arm"]["wrist_down"]):
                self.arm.setWristSpeed(0.9)
            else:
                self.arm.setWristSpeed(0)
        except:
            self.onException()
        # Intake
        try:
            if self.joystick.getRawButton(self.buttons["arm"]["intake_in"]):
                self.arm.setIntakeSpeed(-1.0)
            elif self.joystick.getRawButton(self.buttons["arm"]["intake_out"]):
                self.arm.setIntakeSpeed(1.0)
            else:
                self.arm.setIntakeSpeed(0)
        except:
            self.onException()

    def testInit(self):
        print("Starting Test")

    def testPeriodic(self):
        pass

logging.basicConfig(level=logging.DEBUG)
if __name__ == '__main__':
    wpilib.run(Robot)
