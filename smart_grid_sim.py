import threading
import time
import random

# GRID CONFIGURATION
PRIORITIES = {
    "Hospital": 1,    # Highest Priority
    "Residential": 2, 
    "Industrial": 3   # Lowest Priority
}

class SmartGrid:
    def __init__(self):
        self.total_supply = 0
        self.total_demand = 0
        self.grid_lock = threading.Lock()
        self.running = True

    def update_supply(self, amount):
        with self.grid_lock:
            self.total_supply = max(0, self.total_supply + amount)

    def report_status(self):
        with self.grid_lock:
            status = f"\r[GRID STATUS] Supply: {self.total_supply:.2f}kW | Demand: {self.total_demand:.2f}kW"
            if self.total_supply < self.total_demand:
                status += " | BROWNOUT RISK"
            else:
                status += " | STABLE"
            print(status, end="")

# GENERATOR THREADS
def solar_farm(grid):
    while grid.running:
        # Simulate sun intensity (highest at mid-day)
        generation = random.uniform(20, 100) 
        grid.update_supply(generation)
        time.sleep(2)
        grid.update_supply(-generation) # Reset for next cycle simulation

def wind_turbine(grid):
    while grid.running:
        generation = random.uniform(10, 60)
        grid.update_supply(generation)
        time.sleep(3)
        grid.update_supply(-generation)

# CONSUMER THREADS
def power_consumer(name, priority_level, grid):
    while grid.running:
        demand = random.uniform(15, 40)
        
        with grid.grid_lock:
            # Load Balancing Logic
            if grid.total_supply >= demand:
                # Normal Operation
                grid.total_demand += demand
                can_power = True
            elif priority_level <= 1:
                # Critical Priority Override
                grid.total_demand += demand
                can_power = True
            else:
                # Throttling Low Priority
                can_power = False
        
        if not can_power:
            print(f"\n[!] THROTTLING: {name} disconnected to save grid stability.")
        
        time.sleep(2)
        
        with grid.grid_lock:
            if can_power:
                grid.total_demand -= demand

# MAIN EXECUTION
if __name__ == "__main__":
    my_grid = SmartGrid()
    
    # Initialize Threads
    threads = [
        threading.Thread(target=solar_farm, args=(my_grid,), name="Solar"),
        threading.Thread(target=wind_turbine, args=(my_grid,), name="Wind"),
        threading.Thread(target=power_consumer, args=("City Hospital", 1, my_grid)),
        threading.Thread(target=power_consumer, args=("Residential Zone A", 2, my_grid)),
        threading.Thread(target=power_consumer, args=("Steel Factory", 3, my_grid)),
    ]

    print("Smart Microgrid Multi-Threaded Simulation Starting")
    for t in threads:
        t.start()

    try:
        while True:
            my_grid.report_status()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down grid...")
        my_grid.running = False
        for t in threads:
            t.join()