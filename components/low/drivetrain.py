import ctre

from analog_input import AnalogInput


class Drivetrain:

    front_left: ctre.WPI_TalonSRX
    front_right: ctre.WPI_TalonSRX
    back_left: ctre.WPI_TalonSRX
    back_right: ctre.WPI_TalonSRX
    navx_yaw: AnalogInput

    def __init__(self):
        self.left_speed = 0
        self.right_speed = 0

    def set(self, x, y, twist):
        left_speed = (y + (x if x > 0 else 0) + twist)
        right_speed = (y - (x if x < 0 else 0) - twist)
        # Normalization
        speed_max = max(abs(left_speed), abs(right_speed))
        if speed_max > 1:
            left_speed /= speed_max
            right_speed /= speed_max
        # Set speeds
        self.setSpeeds(left_speed, right_speed)

    def setSpeeds(self, left_speed, right_speed):
        self.left_speed = left_speed
        self.right_speed = right_speed

    def getSpeeds(self):
        return (self.left_speed, self.right_speed)

    def getEncLeft(self):
        return 0

    def getEncRight(self):
        return 0

    def getNavx(self):
        return self.navx_yaw.get()

    def execute(self):
        self.front_left.set(self.left_speed)
        self.front_right.set(self.right_speed)
        self.back_left.set(self.left_speed)
        self.back_right.set(self.right_speed)
