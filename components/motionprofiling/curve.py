class Curve:
    def __init__(self,
                 start,
                 end,
                 min_speed=0.1,
                 max_speed=1.0,
                 max_acc=0.03,
                 reverse=False):
        self.start = start
        self.end = end
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.max_acc = max_acc
        self.reverse = reverse

    def setStart(self, start):
        self.start = start

    def setEnd(self, end):
        self.end = end

    def getStart(self):
        return self.start

    def getEnd(self):
        return self.end

    def getSpeed(self, pos):
        if (self.start < self.end) == self.reverse:
            if pos >= self.start:
                return -self.min_speed
            if pos > self.start - (
                (self.max_speed - self.min_speed) / self.max_acc) and pos > (
                    self.start + self.end) / 2:
                return -(self.min_speed + (pos - self.start) * self.max_acc)
            if pos > self.end + (
                (self.max_speed - self.min_speed) / self.max_acc):
                return -self.max_speed
            if pos > self.end:
                return -(self.min_speed + (self.end - pos) * self.max_acc)
            return 0
        if pos <= self.start:
            return self.min_speed
        if pos < self.start + ((self.max_speed - self.min_speed) / self.max_acc
                               ) and pos < (self.start + self.end) / 2:
            return self.min_speed + (pos - self.start) * self.max_acc
        if pos < self.end - ((self.max_speed - self.min_speed) / self.max_acc):
            return self.max_speed
        if pos < self.end:
            return self.min_speed + (self.end - pos) * self.max_acc
        return 0
