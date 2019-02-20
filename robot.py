import json
import sys
import logging
import magicbot
import wpilib
import ctre
import os

class Robot(magicbot.MagicRobot):

    def createObjects(self):
        self.logger = logging.getLogger("Robot")
        
        # Timer
        self.globalTimer = wpilib.Timer()
        self.globalTimer.start()

        # Load ports and buttons
        with open("../ports.json" if os.getcwd()[-5:-1] == "test" else sys.path[0] + "/ports.json") as f:
            ports = json.load(f)
        with open("../buttons.json" if os.getcwd()[-5:-1] == "test" else sys.path[0] + "/buttons.json") as f:
            self.buttons = json.load(f)
        
        self.liftLimit = wpilib.DigitalInput(ports["lift"]["limit"])

    def teleopInit(self):
        print("Starting Teleop")

    def teleopPeriodic(self):
        if self.globalTimer.hasPeriodPassed(0.5):
            self.logger.info(self.liftLimit.get())

    def testInit(self):
        print("Starting Test")

    def testPeriodic(self):
        pass

logging.basicConfig(level=logging.DEBUG)
if __name__ == '__main__':
    wpilib.run(Robot)
