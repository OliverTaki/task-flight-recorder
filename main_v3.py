from tfr.sampler import Sampler
from tfr.storage_v2 import Storage
from tfr.trigger import Trigger
from tfr.events import EventStore
from tfr.ring_buffer import RingBuffer
from tfr.retention import Retention
from tfr.config import SAMPLE_INTERVAL, RETENTION_HOURS

storage = Storage()
trigger = Trigger()
events = EventStore()
ring = RingBuffer(size=360)
retention = Retention(storage, RETENTION_HOURS)


def handle(data):
    ring.append(data)
    storage.insert(data)

    ev = trigger.check(data)
    if ev:
        window = ring.snapshot()
        for e in ev:
            events.save(e, window)

    retention.cleanup()


if __name__ == '__main__':
    sampler = Sampler(interval=SAMPLE_INTERVAL)
    sampler.run(handle)
