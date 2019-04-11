import random

from components.low.drivetrain import Drivetrain


def test_normalize(robot):
    drive = Drivetrain()
    for _ in range(1000):
        drive.set(random.random() * 2 - 1,
                  random.random() * 2 - 1,
                  random.random() * 2 - 1)
        assert max([abs(x) for x in drive.getSpeeds()]) <= 1
