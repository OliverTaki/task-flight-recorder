import time

class Retention:
    def __init__(self, storage, hours):
        self.storage = storage
        self.seconds = hours * 3600

    def cleanup(self):
        cutoff = time.time() - self.seconds
        self.storage.delete_older_than(cutoff)
