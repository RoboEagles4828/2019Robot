import wpilib


class DriveTrain:

    front_left: wpilib.Spark
    front_right: wpilib.Spark
    back_left: wpilib.Spark
    back_right: wpilib.Spark

    def __init__(self):
        self.speed_left = 0
        self.speed_right = 0

    def setSpeeds(self, speed_left, speed_right):
        self.speed_left = speed_left
        self.speed_right = speed_right

    def setSpeedsFromJoystick(self, x, y, twist):
        speed_left = (-y + (x if x > 0 else 0) + twist)
        speed_right = (-y - (x if x < 0 else 0) - twist)
        # Normalization
        speed_max = max(abs(speed_left), abs(speed_right))
        if speed_max > 1:
            speed_left /= speed_max
            speed_right /= speed_max
        # Set speeds
        self.setSpeeds(speed_left, speed_right)

    def getSpeeds(self):
        return (self.speed_left, self.speed_right)

    def execute(self):
        self.front_left.set(self.speed_left)
        self.front_right.set(self.speed_right)
        self.back_left.set(self.speed_left)
        self.back_right.set(self.speed_right)
