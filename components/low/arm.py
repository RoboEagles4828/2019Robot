import wpilib
import ctre


class Arm:

    arm_left: ctre.WPI_TalonSRX
    arm_right: ctre.WPI_TalonSRX
    wrist: ctre.WPI_VictorSPX
    intake: ctre.WPI_VictorSPX
    hatch_0: wpilib.PWM
    hatch_1: wpilib.PWM
    hatch_2: wpilib.PWM
    wrist_enc: wpilib.AnalogInput
    arm_limit: wpilib.DigitalInput

    def __init__(self):
        self.arm_speed = 0
        self.wrist_speed = 0
        self.intake_speed = 0
        self.hatch_pos = 0
        self.arm_enc_start = 0
        self.wrist_enc_start = 0

    def setup(self):
        self.hatch_0.setBounds(2, 1.55, 1.5, 1.45, 1)
        self.hatch_1.setBounds(2, 1.55, 1.5, 1.45, 1)
        self.hatch_2.setBounds(2, 1.55, 1.5, 1.45, 1)
        self.arm_left.setQuadraturePosition(
            self.arm_left.getPulseWidthPosition())

    def setArmSpeed(self, speed):
        self.arm_speed = speed

    def setWristSpeed(self, speed):
        self.wrist_speed = speed

    def setIntakeSpeed(self, speed):
        self.intake_speed = speed

    def setHatch(self, pos):
        self.hatch_pos = pos

    def getArmSpeed(self):
        return self.arm_speed

    def getWristSpeed(self):
        return self.wrist_speed

    def getArmEnc(self):
        return -self.arm_left.getQuadraturePosition() - self.arm_enc_start

    def setArmEnc(self, pos):
        self.arm_enc_start = -self.arm_left.getQuadraturePosition() - pos

    def getWristEnc(self):
        return self.wrist_enc.getValue() - self.wrist_enc_start

    def setWristEnc(self, pos):
        self.wrist_enc_start = self.wrist_enc.getValue() - pos

    def getArmLimit(self):
        return not self.arm_limit.get()

    def execute(self):
        self.arm_left.set(self.arm_speed)
        self.arm_right.set(self.arm_speed)
        self.wrist.set(self.wrist_speed)
        self.intake.set(self.intake_speed if not self.getArmLimit() else 0)
        self.hatch_0.setPosition(self.hatch_pos)
        self.hatch_1.setPosition(self.hatch_pos)
        self.hatch_2.setPosition(self.hatch_pos)
