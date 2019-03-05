import json
import sys
import logging
import os
import magicbot
import wpilib
import ctre
import navx

from components.low.drivetrain import DriveTrain
from components.low.arm import Arm
from components.motionprofiling.arm_mover import ArmMover
from components.low.lift import Lift
from components.high.lift_mover import LiftMover

class Robot(magicbot.MagicRobot):

    drive: DriveTrain
    arm: Arm
    arm_mover: ArmMover

    arm_speed = 0.3
    wrist_speed = 0.6
    intake_speed = 1.0

    def createObjects(self):
        self.logger = logging.getLogger("Robot")
        # Load ports and buttons
        with open(sys.path[0] + ("/../" if os.getcwd()[-5:-1] == "test" else "/") + "ports.json") as f:
            self.ports = json.load(f)
        with open(sys.path[0] + ("/../" if os.getcwd()[-5:-1] == "test" else "/") + "buttons.json") as f:
            self.buttons = json.load(f)
        # Drive
        self.front_left = ctre.WPI_TalonSRX(self.ports["drive"]["front_left"])
        self.front_right = ctre.WPI_TalonSRX(self.ports["drive"]["front_right"])
        self.back_left = ctre.WPI_TalonSRX(self.ports["drive"]["back_left"])
        self.back_right = ctre.WPI_TalonSRX(self.ports["drive"]["back_right"])
        # Arm
        self.arm_left = ctre.WPI_TalonSRX(self.ports["arm"]["arm_left"])
        self.arm_right = ctre.WPI_TalonSRX(self.ports["arm"]["arm_right"])
        self.wrist = ctre.WPI_VictorSPX(self.ports["arm"]["wrist"])
        self.intake = ctre.WPI_VictorSPX(self.ports["arm"]["intake"])
        self.hatch = wpilib.DoubleSolenoid(self.ports["arm"]["hatch_in"], self.ports["arm"]["hatch_out"])
        self.wrist_enc = wpilib.AnalogInput(self.ports["arm"]["wrist_enc"])
        # Joystick
        self.joystick = wpilib.Joystick(0)
        self.drive_joystick = wpilib.Joystick(1)
        # Timer
        self.timer = wpilib.Timer()
        self.timer.start()
        # Shuffleboard
        self.test_tab = wpilib.shuffleboard.Shuffleboard.getTab("Test")
        # Camera server
        wpilib.CameraServer.launch()

    def teleopInit(self):
        print("Starting Teleop")

    def teleopPeriodic(self):
        # Drive
        try:
            self.drive.setSpeedsFromJoystick(self.drive_joystick.getX(), self.drive_joystick.getY(), self.drive_joystick.getTwist() / 2)
        except:
            self.onException()
        # Arm
        try:
            if self.getButton(self.joystick, "arm", "arm_up"):
                self.arm_mover.disable()
                self.arm.setArmSpeed(self.arm_speed)
            elif self.getButton(self.joystick, "arm", "arm_down"):
                self.arm_mover.disable()
                self.arm.setArmSpeed(-self.arm_speed)
            else:
                if not self.arm_mover.isEnabled():
                    self.arm.setArmSpeed(0)
        except:
            self.onException()
        # Wrist
        try:
            if self.getButton(self.joystick, "arm", "wrist_up"):
                self.arm_mover.disable()
                self.arm.setWristSpeed(self.wrist_speed)
            elif self.getButton(self.joystick, "arm", "wrist_down"):
                self.arm_mover.disable()
                self.arm.setWristSpeed(-self.wrist_speed)
            else:
                if not self.arm_mover.isEnabled():
                    self.arm.setWristSpeed(0)
        except:
            self.onException()
        # Arm mover
        try:
            if self.getButton(self.joystick, "arm", "hatch_in"):
                self.arm_mover.set("hatch_in")
            elif self.getButton(self.joystick, "arm", "hatch_out_1"):
                self.arm_mover.set("hatch_out_1")
            elif self.getButton(self.joystick, "arm", "hatch_out_2"):
                self.arm_mover.set("hatch_out_2")
            elif self.getButton(self.joystick, "arm", "ball_in"):
                self.arm_mover.set("ball_in")
            elif self.getButton(self.joystick, "arm", "ball_out_1"):
                self.arm_mover.set("ball_out_1")
            elif self.getButton(self.joystick, "arm", "ball_out_2"):
                self.arm_mover.set("ball_out_2")
        except:
            self.onException()
        # Intake
        try:
            if self.getButton(self.joystick, "arm", "intake_out"):
                self.arm_mover.disable()
                self.arm.setIntakeSpeed(self.intake_speed)
            elif self.getButton(self.joystick, "arm", "intake_in"):
                self.arm_mover.disable()
                self.arm.setIntakeSpeed(-self.intake_speed)
            else:
                self.arm.setIntakeSpeed(0)
        except:
            self.onException()
        # Hatch
        try:
            self.arm.setHatch(self.getButton(self.joystick, "arm", "hatch"))
        except:
            self.onException()
        # Encoders
        try:
            if self.getButton(self.joystick, "arm", "zero_arm_enc"):
                self.arm.zeroArmEnc()
        except:
            self.onException()

    def testInit(self):
        print("Starting Test")

    def testPeriodic(self):
        self.drive.setSpeeds(0.5, 0)
        self.timer.delay(1)
        self.drive.setSpeeds(0, 0.5)
        self.timer.delay(1)

    def getButton(self, joystick, group, button):
        return joystick.getRawButton(self.buttons[group][button])

logging.basicConfig(level=logging.DEBUG)
if __name__ == '__main__':
    wpilib.run(Robot)
