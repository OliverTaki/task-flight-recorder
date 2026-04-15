import json
import os
import time

class EventStore:
    def __init__(self, path='events'):
        self.path = path
        os.makedirs(self.path, exist_ok=True)

    def save(self, label, window):
        ts = int(time.time())
        fname = f"{label}_{ts}.json"
        full = os.path.join(self.path, fname)
        with open(full, 'w') as f:
            json.dump(window, f)
