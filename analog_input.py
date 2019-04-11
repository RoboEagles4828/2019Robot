class AnalogInput:
    def __init__(self, getter, map_a=1, map_b=0, deadzone=0, average_period=0):
        # Set getter
        self.getter = getter
        # Set map, deadzone, and average period
        self.map_a = map_a
        self.map_b = map_b
        self.deadzone = deadzone
        self.average_period = average_period
        # Set initial value
        self.value = self.get_raw()
        # Create data list
        self.data = [self.value]

    def get_raw(self):
        return self.map_a * self.getter() + self.map_b

    def get(self):
        return self.value

    def update(self):
        # Add data
        self.data.append(self.get_raw())
        # Drop old data
        if len(self.data) > self.average_period + 1:
            self.data.pop(0)
        # Set averaged value
        temp_value = 0
        for value in self.data:
            temp_value += value
        temp_value /= len(self.data)
        # Apply deadzone
        if -self.deadzone < temp_value < self.deadzone:
            self.value = 0
        else:
            self.value = temp_value
