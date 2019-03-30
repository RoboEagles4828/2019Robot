import logging
import json
import sys
import os
import magicbot
import wpilib
import ctre
import navx

from digital_input import DigitalInput
from analog_input import AnalogInput
from components.low.drivetrain import DriveTrain
from components.low.lift import Lift
from components.high.lift_mover import LiftMover
from components.low.dumper import Dumper


class Robot(magicbot.MagicRobot):

    drive: DriveTrain
    lift: Lift
    lift_mover: LiftMover
    dumper: Dumper

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
        self.lift_prox_front = DigitalInput(
            wpilib.DigitalInput(self.ports["lift"]["prox_front"]).get)
        self.lift_prox_back = DigitalInput(
            wpilib.DigitalInput(self.ports["lift"]["prox_back"]).get)
        self.lift_limit_front = DigitalInput(
            wpilib.DigitalInput(self.ports["lift"]["limit_front"]).get)
        self.lift_limit_back = DigitalInput(
            wpilib.DigitalInput(self.ports["lift"]["limit_back"]).get)
        # Hatch
        self.hatch_0 = wpilib.Servo(self.ports["hatch"]["servo_0"])
        self.hatch_1 = wpilib.Servo(self.ports["hatch"]["servo_1"])
        # Dumper
        self.dumper_solenoid = wpilib.DoubleSolenoid(
            self.ports["dumper"]["up"], self.ports["dumper"]["down"])
        self.dumper_servo_0 = wpilib.Servo(self.ports["dumper"]["servo_0"])
        self.dumper_servo_1 = wpilib.Servo(self.ports["dumper"]["servo_1"])
        self.dumper_prox = DigitalInput(
            wpilib.DigitalInput(self.ports["dumper"]["prox"]).get)
        # Navx
        self.navx = navx.ahrs.AHRS.create_spi()
        self.navx_yaw = AnalogInput(
            self.navx.getYaw,
            average_period=self.config["navx"]["average_period"])
        self.navx_roll = AnalogInput(
            self.navx.getRoll,
            average_period=self.config["navx"]["average_period"])
        self.navx_pitch = AnalogInput(
            self.navx.getPitch,
            average_period=self.config["navx"]["average_period"])
        # Joysticks
        self.joystick_0 = wpilib.Joystick(0)
        self.joystick_0_x = AnalogInput(
            self.joystick_0.getX,
            deadzone=self.config["joystick"]["deadzone"],
            average_period=self.config["joystick"]["average_period"])
        self.joystick_0_y = AnalogInput(
            self.joystick_0.getY,
            map_a=-1,
            deadzone=self.config["joystick"]["deadzone"],
            average_period=self.config["joystick"]["average_period"])
        self.joystick_0_twist = AnalogInput(
            self.joystick_0.getTwist,
            map_a=self.config["joystick"]["twist_ratio"],
            deadzone=self.config["joystick"]["deadzone"],
            average_period=self.config["joystick"]["average_period"])
        self.joystick_1 = wpilib.Joystick(1)
        self.joystick_1_x = AnalogInput(
            self.joystick_1.getX,
            deadzone=self.config["joystick"]["deadzone"],
            average_period=self.config["joystick"]["average_period"])
        self.joystick_1_y = AnalogInput(
            self.joystick_1.getY,
            map_a=-1,
            deadzone=self.config["joystick"]["deadzone"],
            average_period=self.config["joystick"]["average_period"])
        self.joystick_1_twist = AnalogInput(
            self.joystick_1.getTwist,
            map_a=self.config["joystick"]["twist_ratio"],
            deadzone=self.config["joystick"]["deadzone"],
            average_period=self.config["joystick"]["average_period"])
        # Timer
        self.timer = wpilib.Timer()
        self.timer.start()
        # CameraServer
        wpilib.CameraServer.launch()
        #cs = cscore.CameraServer.getInstance().startAutomaticCapture(
        #    return_server=True)
        #cs.setFPS(10)
        # LiveWindow
        wpilib.LiveWindow.disableAllTelemetry()

    def teleopInit(self):
        self.navx.reset()

    def teleopPeriodic(self):
        # Drive
        try:
            if (self.joystick_0_x.get(), self.joystick_0_y.get(),
                    self.joystick_0_twist.get()) == (0, 0, 0):
                if not self.lift_mover.isEnabled():
                    self.drive.setSpeeds(0, 0)
            else:
                self.lift_mover.disable()
                self.drive.set(self.joystick_0_x.get(),
                               self.joystick_0_y.get(),
                               self.joystick_0_twist.get())
        except:
            self.onException()
        # Lift
        try:
            if self.getButton("lift", "drive"):
                self.lift_mover.disable()
                self.lift.setDriveSpeed(self.config["lift"]["drive_speed"])
            else:
                if not self.lift_mover.isEnabled():
                    self.lift.setDriveSpeed(0)
            if self.getButton("lift", "front_up"):
                self.lift_mover.disable()
                self.lift.setFrontSpeed(self.config["lift"]["speed"])
            elif self.getButton("lift", "front_down"):
                self.lift_mover.disable()
                self.lift.setFrontSpeed(-self.config["lift"]["speed"])
            else:
                if not self.lift_mover.isEnabled():
                    self.lift.setFrontSpeed(0)
            if self.getButton("lift", "back_up"):
                self.lift_mover.disable()
                self.lift.setBackSpeed(self.config["lift"]["speed"])
            elif self.getButton("lift", "back_down"):
                self.lift_mover.disable()
                self.lift.setBackSpeed(-self.config["lift"]["speed"])
            else:
                if not self.lift_mover.isEnabled():
                    self.lift.setBackSpeed(0)
            if self.getButton("lift", "up"):
                self.lift_mover.disable()
                self.lift_mover.set(self.config["lift"]["speed"])
            elif self.getButton("lift", "down"):
                self.lift_mover.disable()
                self.lift_mover.set(-self.config["lift"]["speed"] / 2)
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
        # Hatch
        try:
            if self.getButton("hatch", "set"):
                self.hatch_0.set(self.config["hatch"]["pos_0_open"])
                self.hatch_1.set(self.config["hatch"]["pos_1_open"])
            else:
                self.hatch_0.set(self.config["hatch"]["pos_0_close"])
                self.hatch_1.set(self.config["hatch"]["pos_1_close"])
        except:
            self.onException()
        # Dumper
        try:
            self.dumper.set(self.getButton("dumper", "set"))
        except:
            self.onException()
        # Debug
        for k, v in self.lift_mover.debug().items():
            wpilib.SmartDashboard.putNumber(k, v)
        wpilib.SmartDashboard.putNumber("Navx Yaw", self.navx_yaw.get())
        wpilib.SmartDashboard.putNumber("Navx Roll", self.navx_roll.get())
        wpilib.SmartDashboard.putNumber("Navx Pitch", self.navx_pitch.get())

    def testInit(self):
        pass

    def testPeriodic(self):
        pass

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
        if joystick.getRawButton(value):
            self.logger.info("Pressed Button " + group + " " + button)
        return joystick.getRawButton(value)


logging.basicConfig(level=logging.DEBUG)
if __name__ == '__main__':
    wpilib.run(Robot)
