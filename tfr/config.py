"""
tfr/config.py — TFR global configuration
All paths are absolute, derived from the project root.
"""
from pathlib import Path

# Project root = parent of this file's directory
PROJECT_DIR = Path(__file__).resolve().parent.parent

# ── File paths ────────────────────────────────────────────────────────────────
DB_PATH    = PROJECT_DIR / "tfr.db"
EVENTS_DIR = PROJECT_DIR / "events"
PID_FILE   = PROJECT_DIR / "tfr.pid"
LOG_FILE   = PROJECT_DIR / "tfr.log"

# ── Sampling ──────────────────────────────────────────────────────────────────
SAMPLE_INTERVAL = 10   # seconds between thin samples

# ── Retention ─────────────────────────────────────────────────────────────────
RETENTION_HOURS = 6    # thin logs kept in DB

# ── Trigger thresholds ────────────────────────────────────────────────────────
CPU_SPIKE_THRESHOLD  = 85          # overall CPU %
PROC_COUNT_SPIKE     = 400         # process count (Windows typically 300-400+)
NET_SPIKE_BYTES      = 50 * 1024 * 1024  # 50 MB delta per sample

# ── Trigger cooldown ──────────────────────────────────────────────────────────
TRIGGER_COOLDOWN_SEC = 60          # same event type fires at most once per 60s

# ── Random snapshot ───────────────────────────────────────────────────────────
RANDOM_SNAPSHOT_INTERVAL_SEC = 3600   # 1 hour
