class RingBuffer:
    def __init__(self, size):
        self.size = size
        self.data = []

    def append(self, item):
        self.data.append(item)
        if len(self.data) > self.size:
            self.data.pop(0)

    def snapshot(self):
        return list(self.data)
