# Smart Microgrid Balancer

## Overview
A multi-threaded simulation of a smart power microgrid with dynamic load balancing. Models concurrent energy generation from renewable sources (solar and wind) and consumption from prioritised consumers, with real-time brownout detection and automatic load shedding.

**Tech Stack:** Python · Threading · Concurrency

---

## How It Works

### Architecture
The simulation runs entirely on concurrent threads, each representing a real-world grid component operating independently and simultaneously:

| Thread | Role | Generation/Demand |
|---|---|---|
| Solar Farm | Generator | 20–100 kW (random, cyclic) |
| Wind Turbine | Generator | 10–60 kW (random, cyclic) |
| City Hospital | Consumer — Priority 1 | 15–40 kW |
| Residential Zone A | Consumer — Priority 2 | 15–40 kW |
| Steel Factory | Consumer — Priority 3 | 15–40 kW |

### Load Balancing Logic
The grid applies a **priority-based load shedding** algorithm when supply is insufficient:

```
IF supply >= demand:
    → Serve all consumers (Normal Operation)
ELIF consumer priority == 1 (Critical):
    → Serve regardless of supply (Critical Override)
ELSE:
    → Throttle consumer (disconnect to protect grid stability)
```

This mirrors real-world grid management where hospitals and emergency services maintain power during brownout conditions while lower-priority loads are shed.

### Thread Safety
All reads and writes to shared grid state (`total_supply`, `total_demand`) are protected by a `threading.Lock()` to prevent race conditions. This ensures grid status reporting is always consistent even under concurrent updates.

---

## Grid Status Output
The simulation prints a live updating status line:

```
[GRID STATUS] Supply: 73.45kW | Demand: 58.20kW | STABLE
[GRID STATUS] Supply: 18.30kW | Demand: 62.10kW | BROWNOUT RISK
[!] THROTTLING: Steel Factory disconnected to save grid stability.
```

---

## Usage

**1. No dependencies required** — uses Python standard library only.

**2. Run the simulation:**
```bash
python smart_grid_sim.py
```

**3. Stop with** `Ctrl+C`, the simulation shuts down cleanly, joining all threads before exit.

---

## Key Concepts Demonstrated
- Multi-threading with `threading.Thread`
- Mutex locks (`threading.Lock`) for shared state protection
- Race condition prevention in concurrent systems
- Priority-based resource allocation algorithms
- Graceful thread shutdown with `join()`
- Real-time simulation of dynamic supply/demand systems

---

## Limitations & Extensions
- Generation values are randomised rather than modelled on real solar/wind irradiance curves. A natural extension would integrate real weather data (as done in the [Solar Energy Prediction](https://github.com/fawazsanu/Solar-Energy-Prediction) project) to drive generation values.
- The simulation runs in real time, a discrete event simulation approach would allow faster-than-real-time modelling.
- Energy storage (batteries) is not modelled, a buffer system would significantly improve brownout resilience.