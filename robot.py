import logging
import json
import sys
import os
import magicbot
import wpilib
import ctre
import navx

from components.low.drivetrain import DriveTrain
from components.low.lift import Lift
from components.high.lift_mover import LiftMover


class Robot(magicbot.MagicRobot):

    drive: DriveTrain
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
        self.navx.reset()

    def teleopPeriodic(self):
        # Drive
        try:
            self.drive.setSpeedsFromJoystick(
                self.joystick_0.getX(), self.joystick_0.getY(),
                self.config["drive"]["twist_ratio"] *
                self.joystick_0.getTwist())
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
                self.lift_mover.set(self.config["lift"]["speed"])
            elif self.getButton("lift", "down"):
                self.lift_mover.set(-self.config["lift"]["speed"])
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
            if self.getButton("lift", "enable"):
                self.lift_mover.enable()
        except:
            self.onException()
        for k, v in self.lift_mover.debug().items():
            wpilib.SmartDashboard.putNumber(k, v)

    def testInit(self):
        pass

    def testPeriodic(self):
        self.drive.setSpeeds(0.5, 0)
        self.timer.delay(1)
        self.drive.setSpeeds(0, 0.5)
        self.timer.delay(1)

    def disabledInit(self):
        self.lift_mover.disable()

    def getJoystickButton(self, group, button):
        for j, groups in self.buttons.items():
            for g, buttons in groups.items():
                if g != group:
                    continue
                for b, v in buttons.items():
                    if b == button:
                        if j == "joystick_0":
                            return (self.joystick_0, v)
                        if j == "joystick_1":
                            return (self.joystick_1, v)
        return (None, None)

    def getButton(self, group, button):
        joystick, value = self.getJoystickButton(group, button)
        if joystick is None:
            raise KeyError(
                "Button '%s' in group '%s' does not exist" % (button, group))
        if value == 13:
            return joystick.getPOV() == 0
        if value == 14:
            return joystick.getPOV() == 90
        if value == 15:
            return joystick.getPOV() == 180
        if value == 16:
            return joystick.getPOV() == 270
        return joystick.getRawButton(value)


logging.basicConfig(level=logging.DEBUG)
if __name__ == '__main__':
    wpilib.run(Robot)
