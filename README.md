# Smart Microgrid Distributed Load Balancer

A multithreaded Python simulation of a priority-based smart power grid, modelling concurrent renewable energy generation and load balancing across consumers with different priority levels.

---

## Overview

This simulation creates a live microgrid where multiple power generators and consumers run as independent threads. When supply is insufficient to meet total demand, the grid applies a priority-based throttling policy — protecting critical infrastructure (e.g., hospitals) while disconnecting lower-priority loads (e.g., industrial consumers).

---

## Features

- **Concurrent generation**: Solar and wind sources run as independent threads with randomised output to simulate real-world variability
- **Priority-based load balancing**: Three-tier consumer priority system (Hospital → Residential → Industrial)
- **Critical priority override**: Priority-1 consumers are always powered, even during brownout conditions
- **Live grid status**: Real-time supply/demand display with brownout risk alerts
- **Graceful shutdown**: `KeyboardInterrupt` cleanly stops all threads

---

## Architecture

```
SmartGrid (shared state, mutex-protected)
├── solar_farm         [Thread] — generates 20–100 kW per cycle (2s)
├── wind_turbine       [Thread] — generates 10–60 kW per cycle (3s)
├── power_consumer     [Thread] — City Hospital    (Priority 1 — Critical)
├── power_consumer     [Thread] — Residential Zone A (Priority 2 — Standard)
└── power_consumer     [Thread] — Steel Factory    (Priority 3 — Low)
```

All access to `total_supply` and `total_demand` is protected by a `threading.Lock` (`grid_lock`) to prevent race conditions.

---

## Priority Levels

| Priority | Label    | Behaviour under shortage         |
|----------|----------|----------------------------------|
| 1        | Critical | Always powered (override)        |
| 2        | Standard | Powered only when supply permits |
| 3        | Low      | First to be throttled            |

---

## Requirements

- Python 3.6+
- Standard library only (`threading`, `time`, `random`)

---

## Usage

```bash
python smart_grid_sim.py
```

The simulation runs continuously, printing a live status line:

```
[GRID STATUS] Supply: 73.45kW | Demand: 62.10kW | STABLE
[!] THROTTLING: Steel Factory disconnected to save grid stability.
```

Press `Ctrl+C` to shut down the grid cleanly.

---

## Design Notes

**Generator cycle model:** Each generator thread adds power to the grid, sleeps for a cycle duration, then subtracts that same amount before generating a new value. This models discrete generation intervals rather than continuous output, a deliberate simplification for simulation clarity.

**Demand accounting:** Consumers hold their demand value in `total_demand` for approximately 2 seconds (simulating power consumption), then release it. The lock ensures the supply-vs-demand check and demand increment are atomic.

**No starvation guarantee for Priority 2:** Standard consumers can be repeatedly throttled if supply consistently falls short. Only Priority 1 is guaranteed service.

---

## Potential Extensions

- Add battery storage as a buffer thread
- Implement time-of-day modelling for solar generation curves
- Log brownout events to a file with timestamps
- Add a `tkinter` or `matplotlib` live dashboard
