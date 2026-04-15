import argparse
import json
from datetime import datetime

def cmd_status():
    info = {
        "name": "Task Flight Recorder",
        "status": "ok",
        "time": datetime.now().isoformat(timespec="seconds"),
        "note": "tfr core loaded"
    }
    print(json.dumps(info, indent=2))

def main():
    parser = argparse.ArgumentParser(prog="tfr")
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("status")
    args = parser.parse_args()

    if args.cmd == "status":
        cmd_status()
        return

    parser.print_help()

if __name__ == "__main__":
    main()
