"""
tfr/trigger.py — Event trigger with per-type cooldown.

Same event type fires at most once per TRIGGER_COOLDOWN_SEC seconds
to prevent spam when a threshold condition persists for multiple samples.
"""
import time
from tfr.config import (
    CPU_SPIKE_THRESHOLD,
    PROC_COUNT_SPIKE,
    NET_SPIKE_BYTES,
    TRIGGER_COOLDOWN_SEC,
)


class Trigger:
    def __init__(self):
        self.last_net  = None
        self._last_fired: dict[str, float] = {}   # event_type -> last fire time

    def _cooldown_ok(self, event_type: str) -> bool:
        """Return True if enough time has passed since this event type last fired."""
        last = self._last_fired.get(event_type, 0.0)
        return (time.time() - last) >= TRIGGER_COOLDOWN_SEC

    def check(self, data: dict) -> list[str]:
        events = []
        now    = time.time()

        if data["cpu_total"] >= CPU_SPIKE_THRESHOLD:
            if self._cooldown_ok("cpu_spike"):
                events.append("cpu_spike")

        if data["proc_count"] >= PROC_COUNT_SPIKE:
            if self._cooldown_ok("proc_spike"):
                events.append("proc_spike")

        if self.last_net is not None:
            delta = data["net_sent"] - self.last_net
            if delta > NET_SPIKE_BYTES and self._cooldown_ok("net_spike"):
                events.append("net_spike")

        self.last_net = data["net_sent"]

        for e in events:
            self._last_fired[e] = now

        return events
