import random

from digital_input import DigitalInput


def test_digital_input(robot):
    value = 0
    prev_value = 0
    test_value = 0
    digital_input = DigitalInput(lambda: value, filter_period=1)
    for _ in range(1000):
        value = random.randint(0, 1)
        digital_input.update()
        if prev_value == value:
            test_value = value
        assert digital_input.get() == test_value
        prev_value = value
