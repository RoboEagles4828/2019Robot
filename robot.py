import logging
import sys
import os
import json
import magicbot
import wpilib
import ctre
import navx

from digital_input import DigitalInput
from analog_input import AnalogInput
from components.low.drivetrain import Drivetrain
from components.low.lift import Lift
from components.low.duck import Duck
from components.low.dumper import Dumper
from components.low.sweeper import Sweeper
from components.high.pathfinder.auto_drive import AutoDrive
from components.high.auto_lift import AutoLift


class Robot(magicbot.MagicRobot):

    drive: Drivetrain
    lift: Lift
    duck: Duck
    dumper: Dumper
    sweeper: Sweeper
    auto_drive: AutoDrive
    auto_lift: AutoLift

    def createObjects(self):
        # Get logger
        self.logger = logging.getLogger("Robot")
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
        # Set MagicRobot constants
        self.control_loop_wait_time = self.config["delay"]
        self.use_teleop_in_autonomous = not self.config["use_auton"]
        # Create input list
        self.inputs = []
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
            wpilib.DigitalInput(self.ports["lift"]["prox_front"]).get,
            filter_period=self.config["lift"]["filter_period"])
        self.lift_prox_back = DigitalInput(
            wpilib.DigitalInput(self.ports["lift"]["prox_back"]).get,
            filter_period=self.config["lift"]["filter_period"])
        self.lift_limit_front = DigitalInput(
            wpilib.DigitalInput(self.ports["lift"]["limit_front"]).get,
            filter_period=self.config["lift"]["filter_period"])
        self.lift_limit_back = DigitalInput(
            wpilib.DigitalInput(self.ports["lift"]["limit_back"]).get,
            filter_period=self.config["lift"]["filter_period"])
        self.inputs.append(self.lift_prox_front)
        self.inputs.append(self.lift_prox_back)
        self.inputs.append(self.lift_limit_front)
        self.inputs.append(self.lift_limit_back)
        # Duck
        self.duck_solenoid = wpilib.DoubleSolenoid(self.ports["pcm"],
                                                   self.ports["duck"]["out"],
                                                   self.ports["duck"]["in"])
        self.duck_servo_0 = wpilib.Servo(self.ports["duck"]["servo_0"])
        self.duck_servo_1 = wpilib.Servo(self.ports["duck"]["servo_1"])
        # Dumper
        self.dumper_solenoid = wpilib.DoubleSolenoid(
            self.ports["pcm"], self.ports["dumper"]["up"],
            self.ports["dumper"]["down"])
        self.dumper_extender = wpilib.DoubleSolenoid(
            self.ports["pcm"], self.ports["dumper"]["extender_out"],
            self.ports["dumper"]["extender_in"])
        self.dumper_servo_0 = wpilib.Servo(self.ports["dumper"]["servo_0"])
        self.dumper_servo_1 = wpilib.Servo(self.ports["dumper"]["servo_1"])
        self.dumper_prox = DigitalInput(
            wpilib.DigitalInput(self.ports["dumper"]["prox"]).get)
        self.inputs.append(self.dumper_prox)
        # Sweeper
        self.sweeper_servo_0 = wpilib.Servo(self.ports["sweeper"]["servo_0"])
        self.sweeper_servo_1 = wpilib.Servo(self.ports["sweeper"]["servo_1"])
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
        self.inputs.append(self.navx_yaw)
        self.inputs.append(self.navx_roll)
        self.inputs.append(self.navx_pitch)
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
        self.inputs.append(self.joystick_0_x)
        self.inputs.append(self.joystick_0_y)
        self.inputs.append(self.joystick_0_twist)
        self.inputs.append(self.joystick_1_x)
        self.inputs.append(self.joystick_1_y)
        self.inputs.append(self.joystick_1_twist)
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
                if not self.auto_lift.isEnabled():
                    self.drive.setSpeeds(0, 0)
            else:
                self.auto_lift.disable()
                self.drive.set(self.joystick_0_x.get(),
                               self.joystick_0_y.get(),
                               self.joystick_0_twist.get())
        except:
            self.onException()
        # Lift
        try:
            if self.getButton("lift", "drive"):
                self.auto_lift.disable()
                self.lift.setDriveSpeed(self.config["lift"]["drive_speed"])
            else:
                if not self.auto_lift.isEnabled():
                    self.lift.setDriveSpeed(0)
            if self.getButton("lift", "front_up"):
                self.auto_lift.disable()
                self.lift.setFrontSpeed(self.config["lift"]["up_speed"])
            elif self.getButton("lift", "front_down"):
                self.auto_lift.disable()
                self.lift.setFrontSpeed(-self.config["lift"]["down_speed"])
            else:
                if not self.auto_lift.isEnabled():
                    self.lift.setFrontSpeed(0)
            if self.getButton("lift", "back_up"):
                self.auto_lift.disable()
                self.lift.setBackSpeed(self.config["lift"]["up_speed"])
            elif self.getButton("lift", "back_down"):
                self.auto_lift.disable()
                self.lift.setBackSpeed(-self.config["lift"]["down_speed"])
            else:
                if not self.auto_lift.isEnabled():
                    self.lift.setBackSpeed(0)
            if self.getButton("lift", "up"):
                self.auto_lift.disable()
                self.auto_lift.set(self.config["lift"]["up_speed"])
            elif self.getButton("lift", "down"):
                self.auto_lift.disable()
                self.auto_lift.set(-self.config["lift"]["down_speed"])
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
        # Duck
        try:
            self.duck.set(self.getButton("duck", "set"))
            self.duck.setServo(
                self.getButton("duck", "set")
                or self.getButton("duck", "set_servo"))
        except:
            self.onException()
        # Dumper
        try:
            self.dumper.set(self.getButton("dumper", "set"))
            self.dumper.setExtender(self.getButton("dumper", "set_extender"))
        except:
            self.onException()
        # Sweeper
        try:
            self.sweeper.set(self.getButton("sweeper", "set"))
        except:
            self.onException()
        # Auto Lift
        try:
            if self.getButton("lift", "enable"):
                self.auto_lift.enable()
        except:
            self.onException()
        # Debug
        for k, v in self.auto_drive.debug().items():
            wpilib.SmartDashboard.putNumber(k, v)
        for k, v in self.auto_lift.debug().items():
            wpilib.SmartDashboard.putNumber(k, v)
        # Update inputs
        for i in self.inputs:
            i.update()

    def testInit(self):
        pass

    def testPeriodic(self):
        pass

    def disabledInit(self):
        self.auto_lift.disable()

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
        wpilib.SmartDashboard.putBoolean("%s : %s" % (group, button),
                                         joystick.getRawButton(value))
        return joystick.getRawButton(value)


logging.basicConfig(level=logging.DEBUG)
if __name__ == '__main__':
    wpilib.run(Robot)
