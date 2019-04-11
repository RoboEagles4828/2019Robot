import random

from analog_input import AnalogInput


def test_analog_input(robot):
    value = 0
    prev_value = 0
    test_value = 0
    analog_input = AnalogInput(
        lambda: value, map_a=2, map_b=-1, deadzone=0.1, average_period=1)
    for _ in range(1000):
        value = random.random()
        analog_input.update()
        test_value = value + prev_value - 1
        if -0.1 < test_value < 0.1:
            test_value = 0
        assert round(analog_input.get(), 4) == round(test_value, 4)
        prev_value = value
