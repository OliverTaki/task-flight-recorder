# Task Flight Recorder

Task Flight Recorder is a lightweight local process telemetry recorder designed to stay out of the way until something goes wrong.

It is not an "AI task manager" and it does not try to decide what is good or bad.
Instead, it continuously captures a thin stream of system state, keeps only a rolling window by default, and preserves denser context around sudden changes so you can inspect what happened later.

## Design goals

- Very light background overhead
- No constant judgment layer
- Rolling retention instead of endless accumulation
- Event bookmarking based on shape change, not semantic interpretation
- Random snapshots for baseline comparison
- SQLite-first storage, CSV export when needed

## Planned v1 scope

- Python implementation
- Lightweight periodic sampling
- System-level totals: CPU, memory, disk I/O, network I/O, process count
- Top CPU and memory processes
- Rolling retention for thin samples
- Event capture around abrupt metric changes
- Random snapshots for baseline comparison
- CSV export
- Simple CLI entrypoint

## Philosophy

This project acts more like a flight recorder than a traditional task manager.
Most of the time it should be quiet, light, and disposable.
Its value appears when you need a factual trail after a slowdown, spike, freeze, or unexplained background activity.

## Status

Repository initialized. Initial v1 scaffold in progress.
