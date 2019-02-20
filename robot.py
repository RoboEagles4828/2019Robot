import json
import sys
import logging
import magicbot
import wpilib
import ctre
import os
import navx

from components.low.lift import Lift

class Robot(magicbot.MagicRobot):

    lift: Lift

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
        self.front_left = wpilib.Spark(ports["drive"]["front_left"])
        self.front_right = wpilib.Spark(ports["drive"]["front_right"])
        self.back_left = wpilib.Spark(ports["drive"]["back_left"])
        self.back_right = wpilib.Spark(ports["drive"]["back_right"])

        # Lift
        self.navx = navx.ahrs.AHRS.create_spi()

        self.lift_front = ctre.WPI_TalonSRX(ports["lift"]["lifter"]["front"])
        self.lift_back = ctre.WPI_TalonSRX(ports["lift"]["lifter"]["back"])

        self.lift_drive_left = wpilib.Victor(ports["lift"]["drive"]["left"])
        self.lift_drive_right = wpilib.Victor(ports["lift"]["drive"]["right"])

        self.lift_top_limit_front = wpilib.DigitalInput(ports["lift"]["limit"]["top_front"])
        self.lift_top_limit_back = wpilib.DigitalInput(ports["lift"]["limit"]["top_back"])
        self.lift_bot_limit_front = wpilib.DigitalInput(ports["lift"]["limit"]["bot_front"])
        self.lift_bot_limit_back = wpilib.DigitalInput(ports["lift"]["limit"]["bot_back"])

        self.lift_prox_front = wpilib.DigitalInput(ports["lift"]["prox"]["front"])
        self.lift_prox_back = wpilib.DigitalInput(ports["lift"]["prox"]["back"])


    def teleopInit(self):
        print("Starting Teleop")

    def teleopPeriodic(self):
        # Drive
        try:
            self.drive.setSpeedsFromJoystick(self.joystick.getX(), self.joystick.getY(), self.joystick.getTwist())
        except:
            self.onException()
        # Arm
        try:
            if self.joystick.getRawButton(self.buttons["joy1"]["liftup"]):
                self.lift.liftUp()
            elif self.joystick.getRawButton(self.buttons["joy1"]["liftdown"]):
                self.lift.liftDown()
            else:
                self.lift.stop()
        except:
            self.onException()

    def testInit(self):
        print("Starting Test")

    def testPeriodic(self):
        pass

logging.basicConfig(level=logging.DEBUG)
if __name__ == '__main__':
    wpilib.run(Robot)
