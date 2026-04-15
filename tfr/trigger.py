import time
from tfr.config import CPU_SPIKE_THRESHOLD, PROC_COUNT_SPIKE, NET_SPIKE_BYTES

class Trigger:
    def __init__(self):
        self.last_net = None

    def check(self, data):
        events = []

        if data['cpu_total'] >= CPU_SPIKE_THRESHOLD:
            events.append('cpu_spike')

        if data['proc_count'] >= PROC_COUNT_SPIKE:
            events.append('proc_spike')

        if self.last_net is not None:
            delta = data['net_sent'] - self.last_net
            if delta > NET_SPIKE_BYTES:
                events.append('net_spike')

        self.last_net = data['net_sent']

        return events
