import json
import sys
import logging
import os
import magicbot
import wpilib
import ctre

from components.low.drivetrain import DriveTrain
from components.low.arm import Arm
from components.motionprofiling.arm_mover import ArmMover

class Robot(magicbot.MagicRobot):

    drive: DriveTrain
    arm: Arm
    arm_mover: ArmMover

    def createObjects(self):
        self.control_loop_wait_time = 0.01
        self.logger = logging.getLogger("Robot")
        # Load ports and buttons
        with open(sys.path[0] + ("/../" if os.getcwd()[-5:-1] == "test" else "/") + "ports.json") as f:
            self.ports = json.load(f)
        with open(sys.path[0] + ("/../" if os.getcwd()[-5:-1] == "test" else "/") + "buttons.json") as f:
            self.buttons = json.load(f)
        with open(sys.path[0] + ("/../" if os.getcwd()[-5:-1] == "test" else "/") + "robot.json") as f:
            self.config = json.load(f)
        # Drive
        self.front_left = wpilib.Spark(self.ports["drive"]["front_left"])
        self.front_right = wpilib.Spark(self.ports["drive"]["front_right"])
        self.back_left = wpilib.Spark(self.ports["drive"]["back_left"])
        self.back_right = wpilib.Spark(self.ports["drive"]["back_right"])
        # Arm
        self.arm_left = ctre.WPI_TalonSRX(self.ports["arm"]["arm_left"])
        self.arm_right = ctre.WPI_TalonSRX(self.ports["arm"]["arm_right"])
        self.wrist = wpilib.Talon(self.ports["arm"]["wrist"])
        self.intake = ctre.WPI_VictorSPX(self.ports["arm"]["intake"])
        self.hatch = wpilib.DoubleSolenoid(self.ports["arm"]["hatch_in"], self.ports["arm"]["hatch_out"])
        self.wrist_enc = wpilib.AnalogInput(self.ports["arm"]["wrist_enc"])
        # Joystick
        self.joystick = wpilib.Joystick(0)
        self.drive_joystick = wpilib.Joystick(1)
        # Timer
        self.timer = wpilib.Timer()
        self.timer.start()
        # Camera server
        wpilib.CameraServer.launch()

    def teleopInit(self):
        print("Starting Teleop")
        self.arm.setArmEnc()

    def teleopPeriodic(self):
        # Drive
        try:
            self.drive.setSpeedsFromJoystick(self.drive_joystick.getX(), self.drive_joystick.getY(), self.drive_joystick.getTwist() / 1.5)
        except:
            self.onException()
        # Arm
        try:
            if self.getButton(self.joystick, "arm", "arm_up"):
                self.arm_mover.disable()
                self.arm.setArmSpeed(self.config["arm"]["arm_speed"])
            elif self.getButton(self.joystick, "arm", "arm_down"):
                self.arm_mover.disable()
                self.arm.setArmSpeed(-self.config["arm"]["arm_speed"])
            else:
                if not self.arm_mover.isEnabled():
                    self.arm.setArmSpeed(0)
        except:
            self.onException()
        # Wrist
        try:
            self.arm.setWristSpeed(self.config["arm"]["wrist_speed"] * self.joystick.getY()
                                   if abs(self.joystick.getY()) > self.config["arm"]["joystick_deadzone"] else 0)
        except:
            self.onException()
        # Arm mover
        try:
            if self.getButton(self.drive_joystick, "arm", "hatch_in"):
                self.arm_mover.set("hatch_in")
            elif self.getButton(self.drive_joystick, "arm", "hatch_out_1"):
                self.arm_mover.set("hatch_out_1")
            elif self.getButton(self.drive_joystick, "arm", "hatch_out_2"):
                self.arm_mover.set("hatch_out_2")
            elif self.getButton(self.drive_joystick, "arm", "ball_in"):
                self.arm_mover.set("ball_in")
            elif self.getButton(self.drive_joystick, "arm", "ball_out_1"):
                self.arm_mover.set("ball_out_1")
            elif self.getButton(self.drive_joystick, "arm", "ball_out_2"):
                self.arm_mover.set("ball_out_2")
        except:
            self.onException()
        # Intake
        try:
            if self.getButton(self.joystick, "arm", "intake_out"):
                self.arm_mover.disable()
                self.arm.setIntakeSpeed(self.config["arm"]["intake_out_speed"])
            elif self.getButton(self.joystick, "arm", "intake_in"):
                self.arm_mover.disable()
                self.arm.setIntakeSpeed(-self.config["arm"]["intake_in_speed"])
            else:
                self.arm.setIntakeSpeed(0)
        except:
            self.onException()
        # Hatch
        try:
            self.arm.setHatch(self.getButton(self.joystick, "arm", "hatch"))
        except:
            self.onException()
        wpilib.SmartDashboard.putString("Arm", self.arm_mover.debug())

    def testInit(self):
        print("Starting Test")

    def testPeriodic(self):
        self.drive.setSpeeds(0.5, 0)
        self.timer.delay(1)
        self.drive.setSpeeds(0, 0.5)
        self.timer.delay(1)

    def disabledInit(self):
        self.arm_mover.disable()

    def getButton(self, joystick, group, button):
        if self.buttons[group][button] == 13:
            return joystick.getPOV() == 0
        if self.buttons[group][button] == 14:
            return joystick.getPOV() == 180
        return joystick.getRawButton(self.buttons[group][button])

logging.basicConfig(level=logging.DEBUG)
if __name__ == '__main__':
    wpilib.run(Robot)
