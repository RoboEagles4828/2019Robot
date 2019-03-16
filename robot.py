import logging
import json
import sys
import os
import magicbot
import wpilib
import navx

from components.low.drivetrain import DriveTrain


class Robot(magicbot.MagicRobot):

    drive: DriveTrain

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
        self.front_left = wpilib.Spark(self.ports["drive"]["front_left"])
        self.front_right = wpilib.Spark(self.ports["drive"]["front_right"])
        self.back_left = wpilib.Spark(self.ports["drive"]["back_left"])
        self.back_right = wpilib.Spark(self.ports["drive"]["back_right"])
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

    def testInit(self):
        pass

    def testPeriodic(self):
        self.drive.setSpeeds(0.5, 0)
        self.timer.delay(1)
        self.drive.setSpeeds(0, 0.5)
        self.timer.delay(1)

    def disabledInit(self):
        pass

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
