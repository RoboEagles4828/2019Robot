import logging

from components.motionprofiling.arm_mover import ArmMover

logging.basicConfig(level=logging.DEBUG)

class FakeArm:

    def __init__(self):
        self.arm_pos = 0
        self.arm_speed = 0
        self.wrist_pos = 0
        self.wrist_speed = 0

    def setArmSpeed(self, speed):
        self.arm_speed = speed

    def setWristSpeed(self, speed):
        self.wrist_speed = speed

    def getArmSpeed(self):
        return self.arm_speed

    def getWristSpeed(self):
        return self.wrist_speed

    def getArmEnc(self):
        return self.arm_pos

    def getWristEnc(self):
        return self.wrist_pos

    def execute(self):
        self.arm_pos += self.arm_speed * 30
        self.wrist_pos += self.wrist_speed * 30

def test_arm_mover(robot):
    arm = FakeArm()
    arm_mover = ArmMover()
    arm_mover.arm = arm
    # Set arm mover position
    arm_mover.set("ball_out_1")
    # Execute loop
    for _ in range(1000):
        arm.execute()
        arm_mover.execute()
        # Check speeds
        assert abs(arm_mover.arm_speed) <= 1
        assert abs(arm_mover.wrist_speed) <= 1
        # Print debug
        logging.info(arm_mover.debug())
    # Check if the positions were reached
    assert abs(arm_mover.config["arm"]["set"][arm_mover.pos] - arm_mover.arm_pos) < 10
    assert abs(arm_mover.config["wrist"]["set"][arm_mover.pos] - arm_mover.wrist_pos) < 10
