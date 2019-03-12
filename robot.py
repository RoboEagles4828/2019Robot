import logging
import json
import sys
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
    lift: Lift
    lift_mover: LiftMover

    def createObjects(self):
        # Get logger
        self.logger = logging.getLogger("Robot")
        # Set MagicRobot constants
        self.control_loop_wait_time = 0.03
        self.use_teleop_in_autonomous = True
        # Load ports, buttons, and config
        with open(sys.path[0] +
                  ("/../" if os.getcwd()[-5:-1] == "test" else "/") +
                  "config/ports.json") as f:
            self.ports = json.load(f)
        with open(sys.path[0] +
                  ("/../" if os.getcwd()[-5:-1] == "test" else "/") +
                  "config/buttons.json") as f:
            self.buttons = json.load(f)
        with open(sys.path[0] +
                  ("/../" if os.getcwd()[-5:-1] == "test" else "/") +
                  "config/robot.json") as f:
            self.config = json.load(f)
        # Drive
        self.drive_front_left = ctre.WPI_TalonSRX(
            self.ports["drive"]["front_left"])
        self.drive_front_right = ctre.WPI_TalonSRX(
            self.ports["drive"]["front_right"])
        self.drive_back_left = ctre.WPI_TalonSRX(
            self.ports["drive"]["back_left"])
        self.drive_back_right = ctre.WPI_TalonSRX(
            self.ports["drive"]["back_right"])
        # Arm
        self.arm_arm_left = ctre.WPI_TalonSRX(self.ports["arm"]["arm_left"])
        self.arm_arm_right = ctre.WPI_TalonSRX(self.ports["arm"]["arm_right"])
        self.arm_wrist = ctre.WPI_VictorSPX(self.ports["arm"]["wrist"])
        self.arm_intake = ctre.WPI_VictorSPX(self.ports["arm"]["intake"])
        self.arm_hatch_0 = wpilib.PWM(self.ports["arm"]["hatch_0"])
        self.arm_hatch_1 = wpilib.PWM(self.ports["arm"]["hatch_1"])
        self.arm_hatch_2 = wpilib.PWM(self.ports["arm"]["hatch_2"])
        self.arm_wrist_enc = wpilib.AnalogInput(self.ports["arm"]["wrist_enc"])
        self.arm_limit = wpilib.DigitalInput(self.ports["arm"]["limit"])
        # Lift
        self.lift_drive_left = ctre.WPI_VictorSPX(
            self.ports["lift"]["drive_left"])
        self.lift_drive_right = ctre.WPI_VictorSPX(
            self.ports["lift"]["drive_right"])
        self.lift_front = ctre.WPI_TalonSRX(self.ports["lift"]["front"])
        self.lift_back = ctre.WPI_TalonSRX(self.ports["lift"]["back"])
        self.lift_prox_front = wpilib.DigitalInput(
            self.ports["lift"]["prox_front"])
        self.lift_prox_back = wpilib.DigitalInput(
            self.ports["lift"]["prox_back"])
        self.lift_limit_front = wpilib.DigitalInput(
            self.ports["lift"]["limit_front"])
        self.lift_limit_back = wpilib.DigitalInput(
            self.ports["lift"]["limit_back"])
        # Navx
        self.navx = navx.ahrs.AHRS.create_spi()
        # Joysticks
        self.joystick_0 = wpilib.Joystick(0)
        self.joystick_1 = wpilib.Joystick(1)
        # Timer
        self.timer = wpilib.Timer()
        self.timer.start()
        # CameraServer
        wpilib.CameraServer.launch()
        # LiveWindow
        wpilib.LiveWindow.disableAllTelemetry()

    def teleopInit(self):
        self.arm.setArmEnc()
        self.navx.reset()

    def teleopPeriodic(self):
        # Drive
        try:
            self.drive.setSpeedsFromJoystick(
                self.drive_joystick.getX(), self.drive_joystick.getY(),
                self.config["drive"]["twist_ratio"] *
                self.drive_joystick.getTwist())
        except:
            self.onException()
        # Arm
        try:
            if self.getButton("arm", "arm_up"):
                self.arm_mover.disable()
                self.arm.setArmSpeed(self.config["arm"]["arm_speed"])
            elif self.getButton("arm", "arm_down"):
                self.arm_mover.disable()
                self.arm.setArmSpeed(-self.config["arm"]["arm_speed"])
            else:
                if not self.arm_mover.isEnabled():
                    self.arm.setArmSpeed(0)
        except:
            self.onException()
        # Wrist
        try:
            self.arm.setWristSpeed(
                self.config["arm"]["wrist_speed"] *
                -self.joystick.getY() if abs(self.joystick.getY(
                )) > self.config["joystick_deadzone"] else 0)
        except:
            self.onException()
        # Arm mover
        try:
            if self.getButton("arm", "hatch_0"):
                self.arm_mover.set("hatch_0")
            elif self.getButton("arm", "hatch_1"):
                self.arm_mover.set("hatch_1")
            elif self.getButton("arm", "hatch_2"):
                self.arm_mover.set("hatch_2")
            elif self.getButton("arm", "ball_0"):
                self.arm_mover.set("ball_0")
            elif self.getButton("arm", "ball_1"):
                self.arm_mover.set("ball_1")
            elif self.getButton("arm", "ball_2"):
                self.arm_mover.set("ball_2")
        except:
            self.onException()
        # Intake
        try:
            if self.getButton("arm", "intake_out"):
                self.arm_mover.disable()
                self.arm.setIntakeSpeed(self.config["arm"]["intake_out_speed"])
            elif self.getButton("arm", "intake_in"):
                self.arm_mover.disable()
                self.arm.setIntakeSpeed(-self.config["arm"]["intake_in_speed"])
            else:
                self.arm.setIntakeSpeed(0)
        except:
            self.onException()
        # Hatch
        try:
            self.arm.setHatch(self.getButton("arm", "hatch"))
            if self.getButton(
                    "arm", "hatch") and (abs(x)
                                         for x in self.drive.getSpeeds()) < (
                                             self.config["joystick_deadzone"],
                                             self.config["joystick_deadzone"]):
                self.drive.setSpeeds(-self.config["drive"]["hatch_speed"],
                                     -self.config["drive"]["hatch_speed"])
        except:
            self.onException()
        # Lift
        try:
            if self.getButton("lift", "drive"):
                self.lift.setDriveSpeed(self.config["lift"]["drive_speed"])
            else:
                self.lift.setDriveSpeed(0)
            if self.getButton("lift", "front_up"):
                self.lift.setFrontSpeed(self.config["lift"]["speed"])
            elif self.getButton("lift", "front_down"):
                self.lift.setFrontSpeed(-self.config["lift"]["speed"])
            else:
                self.lift.setFrontSpeed(0)
            if self.getButton("lift", "back_up"):
                self.lift.setBackSpeed(self.config["lift"]["speed"])
            elif self.getButton("lift", "back_down"):
                self.lift.setBackSpeed(-self.config["lift"]["speed"])
            else:
                self.lift.setBackSpeed(0)
            if self.getButton("lift", "up"):
                self.lift.setLiftSpeed(self.config["lift"]["speed"])
            elif self.getButton("lift", "down"):
                self.lift.setLiftSpeed(-self.config["lift"]["speed"])
            if self.getButton("lift", "front_pos_up"):
                self.lift.setFrontPos(1)
            elif self.getButton("lift", "front_pos_down"):
                self.lift.setFrontPos(-1)
            if self.getButton("lift", "back_pos_up"):
                self.lift.setBackPos(1)
            elif self.getButton("lift", "back_pos_down"):
                self.lift.setBackPos(-1)
        except:
            self.onException()
        # Lift mover
        try:
            if self.getButton("lift", "auto"):
                self.lift_mover.enable()
        except:
            self.onException()
        for k, v in self.arm_mover.debug().items():
            wpilib.SmartDashboard.putNumber(k, v)
        for k, v in self.lift_mover.debug().items():
            wpilib.SmartDashboard.putNumber(k, v)
        wpilib.SmartDashboard.putNumber("Navx", self.navx.getYaw())

    def testInit(self):
        pass

    def testPeriodic(self):
        self.drive.setSpeeds(0.5, 0)
        self.timer.delay(1)
        self.drive.setSpeeds(0, 0.5)
        self.timer.delay(1)

    def disabledInit(self):
        self.arm_mover.disable()
        self.lift_mover.disable()

    def getButton(self, group, button):
        for j, g, b in self.buttons:
            if g == group and b == button:
                joystick_name = j
        if joystick_name == "joystick_0":
            joystick = self.joystick_0
        elif joystick_name == "joystick_1":
            joystick = self.joystick_1
        else:
            return -1
        if self.buttons[joystick_name][group][button] == 13:
            return joystick.getPOV() == 0
        if self.buttons[joystick_name][group][button] == 14:
            return joystick.getPOV() == 90
        if self.buttons[joystick_name][group][button] == 15:
            return joystick.getPOV() == 180
        if self.buttons[joystick_name][group][button] == 16:
            return joystick.getPOV() == 270
        return joystick.getRawButton(
            self.buttons[joystick_name][group][button])


logging.basicConfig(level=logging.DEBUG)
if __name__ == '__main__':
    wpilib.run(Robot)
