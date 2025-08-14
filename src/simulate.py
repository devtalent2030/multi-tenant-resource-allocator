# =============================================================================
# Project: Multi-Tenant Resource Allocator Simulation
# File: simulate.py
# Author: Talent Nyota
# Date: 2025-08-13
# Description: Main simulation loop. Runs minute-by-minute allocation, records 
#              metrics, saves results to CSV, and optionally generates plots.
# =============================================================================

"""
Main driver for the multi-tenant resource allocation simulation.
Simulates minute-by-minute demand, allocation, metrics, and optional plots.
"""

import argparse
import logging
import pandas as pd
from workloads import tenant_a_demand, tenant_b_demand
from allocator import allocate
from metrics import make_tick_row, jain_index

# Capacity and pricing
TOTAL_VCPU = 32
TOTAL_RAM_GB = 64
PRICE_PER_VCPU_HR = 0.04
PRICE_PER_RAM_GB_HR = 0.005

# Floors (minimum guarantees)
A_CPU_FLOOR = 7
A_RAM_FLOOR = 9
B_CPU_FLOOR = 5
B_RAM_FLOOR = 7

# Flash-sale window for Tenant A (keep consistent with workloads.py)
FLASH_START = 27
FLASH_END = 43

def weights_for_minute(t: int) -> tuple[float, float]:
    """Return (A_weight, B_weight) for minute t."""
    if FLASH_START <= t < FLASH_END:
        return 1.6, 1.0
    return 1.0, 1.0

def parse_args() -> argparse.Namespace:
    """CLI arguments for simulation length, logging, CSV, and plotting."""
    p = argparse.ArgumentParser(description="Multi-tenant allocator simulation")
    p.add_argument("--minutes", type=int, default=120, help="simulation length (minutes)")
    p.add_argument("--log", default="INFO", help="log level: DEBUG/INFO/WARNING/ERROR")
    p.add_argument("--csv", default="sim_output.csv", help="output CSV path")
    p.add_argument("--plots", action="store_true", help="generate PNG plots")
    return p.parse_args()

def main() -> None:
    args = parse_args()
    lvl = getattr(logging, args.log.upper(), logging.INFO)
    logging.basicConfig(level=lvl, format="%(levelname)s %(message)s")

    rows = []

    for t in range(args.minutes):
        # Demand per tenant
        a_cpu_need, a_ram_need = tenant_a_demand(t)
        b_cpu_need, b_ram_need = tenant_b_demand(t)

        # Per-minute weights
        a_w, b_w = weights_for_minute(t)

        # Allocation step
        alloc = allocate(
            a_need=(a_cpu_need, a_ram_need),
            b_need=(b_cpu_need, b_ram_need),
            total_cpu=TOTAL_VCPU,
            total_ram=TOTAL_RAM_GB,
            floors=(A_CPU_FLOOR, A_RAM_FLOOR, B_CPU_FLOOR, B_RAM_FLOOR),
            weights=(a_w, b_w)
        )

        # Fairness metric for CPU
        fairness_cpu = jain_index([alloc["a_cpu"], alloc["b_cpu"]])

        # Log edges of special windows
        if t in (FLASH_START - 1, FLASH_START, FLASH_END - 1, FLASH_END):
            logging.info(f"t={t} weights=({a_w},{b_w}) alloc={alloc}")

        # Build row
        row = make_tick_row(
            t=t,
            a_need_cpu=a_cpu_need, a_need_ram=a_ram_need,
            b_need_cpu=b_cpu_need, b_need_ram=b_ram_need,
            a_alloc_cpu=alloc["a_cpu"], a_alloc_ram=alloc["a_ram"],
            b_alloc_cpu=alloc["b_cpu"], b_alloc_ram=alloc["b_ram"],
            price_cpu=PRICE_PER_VCPU_HR,
            price_ram=PRICE_PER_RAM_GB_HR,
            cpu_fairness=fairness_cpu
        )
        rows.append(row)

    # Persist results
    df = pd.DataFrame(rows)
    df.to_csv(args.csv, index=False)
    logging.info(f"wrote {args.csv} with {len(df)} rows")

    # Optional plots
    if args.plots:
        try:
            from plotting import make_plots
            make_plots(args.csv)
        except Exception as e:
            logging.warning(f"plotting skipped: {e}")

if __name__ == "__main__":
    main()
