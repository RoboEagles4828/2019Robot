import logging
import matplotlib.pyplot as plt

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
    # Initialize data
    arm_pos_speed = []
    arm_err = []
    arm_base_speed = []
    arm_speed = []
    wrist_pos_speed = []
    wrist_err = []
    wrist_base_speed = []
    wrist_speed = []
    # Set arm mover position
    arm_mover.set("ball_out_1")
    # Execute loop
    for _ in range(2000):
        arm.execute()
        arm_mover.execute()
        # Add data
        arm_pos_speed.append(arm_mover.arm_pos_speed)
        arm_err.append(arm_mover.arm_err)
        arm_base_speed.append(arm_mover.arm_base_speed)
        arm_speed.append(arm_mover.arm_speed)
        wrist_pos_speed.append(arm_mover.wrist_pos_speed)
        wrist_err.append(arm_mover.wrist_err)
        wrist_base_speed.append(arm_mover.wrist_base_speed)
        wrist_speed.append(arm_mover.wrist_speed)
        # Check speeds
        assert abs(arm_mover.arm_speed) <= 1
        assert abs(arm_mover.wrist_speed) <= 1
        if arm_mover.arm_base_speed == 0 and arm_mover.wrist_speed == 0:
            break
    # Check if the positions were reached
    if abs(arm_mover.config["arm"]["set"][arm_mover.pos] - arm_mover.arm_pos) > 10:
        plt.plot(arm_pos_speed, label="Arm Pos Speed")
        plt.plot(arm_err, label="Arm Err")
        plt.plot(arm_base_speed, label="Arm Base Speed")
        plt.plot(arm_speed, label="Arm Speed")
        plt.legend()
        plt.show()
        assert False
    if abs(arm_mover.config["wrist"]["set"][arm_mover.pos] - arm_mover.wrist_pos) > 10:
        plt.plot(wrist_pos_speed, label="Wrist Pos Speed")
        plt.plot(wrist_err, label="Wrist Err")
        plt.plot(wrist_base_speed, label="Wrist Base Speed")
        plt.plot(wrist_speed, label="Wrist Speed")
        plt.legend()
        plt.show()
        assert False
