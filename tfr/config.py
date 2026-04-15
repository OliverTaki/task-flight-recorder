# Minimal config tuned for low overhead

SAMPLE_INTERVAL = 10  # seconds
RETENTION_HOURS = 6   # thin logs kept

# very conservative trigger (only big spikes)
CPU_SPIKE_THRESHOLD = 85
PROC_COUNT_SPIKE = 50
NET_SPIKE_BYTES = 50 * 1024 * 1024  # 50MB delta

# snapshot
RANDOM_SNAPSHOT_INTERVAL_SEC = 3600  # 1 hour
