"""
tfr/cli.py — Task Flight Recorder CLI
Commands: start | stop | status | log
"""
import argparse
import json
import sqlite3
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

from tfr.config import DB_PATH, EVENTS_DIR, LOG_FILE, PID_FILE, PROJECT_DIR


# ── PID helpers ───────────────────────────────────────────────────────────────

def _read_pid():
    try:
        return int(PID_FILE.read_text().strip())
    except Exception:
        return None


def _is_alive(pid):
    if pid is None:
        return False
    try:
        import psutil
        p = psutil.Process(pid)
        return p.status() not in (psutil.STATUS_ZOMBIE, psutil.STATUS_DEAD)
    except Exception:
        return False


# ── start ─────────────────────────────────────────────────────────────────────

def cmd_start():
    pid = _read_pid()
    if _is_alive(pid):
        print(json.dumps({"status": "already_running", "pid": pid}, indent=2))
        return

    recorder = PROJECT_DIR / "main_v3.py"
    if not recorder.exists():
        print(json.dumps({"status": "error",
                          "message": f"recorder not found: {recorder}"}, indent=2))
        sys.exit(1)

    log_fh = open(LOG_FILE, "a")

    if sys.platform == "win32":
        DETACHED_PROCESS      = 0x00000008
        CREATE_NEW_PROC_GROUP = 0x00000200
        proc = subprocess.Popen(
            [sys.executable, str(recorder)],
            creationflags=DETACHED_PROCESS | CREATE_NEW_PROC_GROUP,
            stdout=log_fh, stderr=log_fh,
            cwd=str(PROJECT_DIR),
        )
    else:
        proc = subprocess.Popen(
            [sys.executable, str(recorder)],
            stdout=log_fh, stderr=log_fh,
            cwd=str(PROJECT_DIR),
            start_new_session=True,
        )

    PID_FILE.write_text(str(proc.pid))
    time.sleep(0.6)

    if _is_alive(proc.pid):
        print(json.dumps({"status": "started", "pid": proc.pid}, indent=2))
    else:
        print(json.dumps({"status": "failed", "pid": proc.pid,
                          "message": "process exited immediately — check tfr.log"},
                         indent=2))
        sys.exit(1)


# ── stop ──────────────────────────────────────────────────────────────────────

def cmd_stop():
    pid = _read_pid()
    if not _is_alive(pid):
        if PID_FILE.exists():
            PID_FILE.unlink()
        print(json.dumps({"status": "not_running"}, indent=2))
        return

    try:
        import psutil
        proc = psutil.Process(pid)
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except psutil.TimeoutExpired:
            proc.kill()
        if PID_FILE.exists():
            PID_FILE.unlink()
        print(json.dumps({"status": "stopped", "pid": pid}, indent=2))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}, indent=2))
        sys.exit(1)


# ── status ────────────────────────────────────────────────────────────────────

def cmd_status():
    pid     = _read_pid()
    running = _is_alive(pid)
    now     = time.time()

    info = {
        "name":    "Task Flight Recorder",
        "running": running,
        "pid":     pid if running else None,
        "time":    datetime.now().isoformat(timespec="seconds"),
    }

    if running:
        try:
            import psutil
            create_time = psutil.Process(pid).create_time()
            sec = int(now - create_time)
            h, r = divmod(sec, 3600); m, s = divmod(r, 60)
            info["uptime"] = f"{h}h {m}m {s}s"
        except Exception:
            pass

    try:
        info["db_path"]    = str(DB_PATH)
        info["db_size_kb"] = round(DB_PATH.stat().st_size / 1024, 1) if DB_PATH.exists() else 0
        if DB_PATH.exists():
            conn = sqlite3.connect(str(DB_PATH))
            row  = conn.execute("SELECT COUNT(*), MAX(timestamp) FROM samples").fetchone()
            conn.close()
            info["sample_count"] = row[0] or 0
            if row[1]:
                info["last_sample"]         = datetime.fromtimestamp(row[1]).isoformat(timespec="seconds")
                info["last_sample_age_sec"] = int(now - row[1])
            else:
                info["last_sample"] = None
        else:
            info["sample_count"] = 0
            info["last_sample"]  = None
    except Exception as e:
        info["db_error"] = str(e)

    try:
        info["event_files"] = len(list(EVENTS_DIR.glob("*.json"))) if EVENTS_DIR.exists() else 0
    except Exception:
        info["event_files"] = 0

    print(json.dumps(info, indent=2))


# ── log ───────────────────────────────────────────────────────────────────────

def cmd_log(n: int, spike_only: bool):
    """Print recent samples as a human-readable table."""
    if not DB_PATH.exists():
        print("No database found.")
        return

    conn = sqlite3.connect(str(DB_PATH))
    where = "WHERE cpu > 50" if spike_only else ""
    rows  = conn.execute(f"""
        SELECT timestamp, cpu, mem, proc_count, top_cpu
        FROM samples {where}
        ORDER BY timestamp DESC LIMIT ?
    """, (n,)).fetchall()
    conn.close()

    if not rows:
        print("No samples found.")
        return

    print(f"{'Time':10}  {'CPU':>6}  {'MEM':>6}  {'Procs':>5}  Top process")
    print("-" * 65)
    for r in reversed(rows):
        dt   = datetime.fromtimestamp(r[0]).strftime("%H:%M:%S")
        top  = json.loads(r[4])
        name = top[0]["name"]        if top else "-"
        pct  = top[0]["cpu_percent"] if top else 0.0
        # cpu_percent from psutil is multi-core (can exceed 100%)
        # Normalize to single-core equivalent for readability
        pct_disp = f"{pct:.0f}%" if pct < 200 else f"{pct/100:.0f}c"
        print(f"{dt}  {r[1]:5.1f}%  {r[2]:5.1f}%  {r[3]:5d}  {name}({pct_disp})")


# ── entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(prog="tfr",
                                     description="Task Flight Recorder CLI")
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("start",  help="Start the recorder in the background")
    sub.add_parser("stop",   help="Stop the recorder")
    sub.add_parser("status", help="Show recorder status and DB stats")

    p_log = sub.add_parser("log", help="Print recent samples")
    p_log.add_argument("-n", type=int, default=20,
                       help="Number of samples to show (default: 20)")
    p_log.add_argument("--spike", action="store_true",
                       help="Show only samples where CPU > 50%%")

    args = parser.parse_args()

    if args.cmd == "start":
        cmd_start()
    elif args.cmd == "stop":
        cmd_stop()
    elif args.cmd == "status":
        cmd_status()
    elif args.cmd == "log":
        cmd_log(n=args.n, spike_only=args.spike)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
