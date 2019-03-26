class DigitalInput:
    def __init__(self, getter, filter_period=0):
        # Set getter
        self.getter = getter
        # Set filter period
        self.filter_period = filter_period
        # Set initial value
        self.value = self.get_raw()
        # Create data list
        self.data = [self.value]

    def get_raw(self):
        return bool(self.getter())

    def get(self):
        return self.value

    def execute(self):
        # Add data
        self.data.append(self.get_raw())
        # Drop old data
        if len(self.data) > self.filter_period + 1:
            self.data.pop(0)
        # Set filtered value
        if (True not in self.data) or (False not in self.data):
            self.value = self.data[0]
