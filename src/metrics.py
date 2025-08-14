# =============================================================================
# Project: Multi-Tenant Resource Allocator Simulation
# File: metrics.py
# Author: Talent Nyota
# Date: 2025-08-13
# Description: Provides functions to calculate SLA compliance, fairness metrics 
#              (e.g., Jain's index), and per-minute cost for resource usage.
# =============================================================================

"""
Metrics and helper functions for SLA tracking, cost estimation,
and fairness evaluation in the simulation.
"""

import numpy as np

def jain_index(values):
    """
    Calculate Jain's fairness index for a list of resource allocations.

    Args:
        values (list or array): Resource allocations per tenant.

    Returns:
        float: Jain's index value (0 to 1), where 1 is perfectly fair.
    """
    v = np.array(values, dtype=float)
    s = v.sum()
    if s == 0:
        return 1.0
    return (s * s) / (len(v) * (v * v).sum())

def cost_for_tick(cpu_alloc, ram_alloc, price_cpu_hr, price_ram_hr):
    """
    Compute cost for a single simulation tick (1 minute).

    Args:
        cpu_alloc (float): CPU allocated (vCPUs).
        ram_alloc (float): RAM allocated (GB).
        price_cpu_hr (float): Hourly cost per vCPU.
        price_ram_hr (float): Hourly cost per GB RAM.

    Returns:
        float: Cost for the tick in currency units.
    """
    minutes_to_hours = 1.0 / 60.0
    cpu_cost = cpu_alloc * price_cpu_hr * minutes_to_hours
    ram_cost = ram_alloc * price_ram_hr * minutes_to_hours
    return cpu_cost + ram_cost

def make_tick_row(t,
                  a_need_cpu, a_need_ram,
                  b_need_cpu, b_need_ram,
                  a_alloc_cpu, a_alloc_ram,
                  b_alloc_cpu, b_alloc_ram,
                  price_cpu, price_ram,
                  cpu_fairness):
    """
    Build a dictionary summarizing all metrics for a simulation tick.

    Returns:
        dict: Row data including demand, allocation, SLA status, costs, and fairness.
    """
    a_ok = (a_alloc_cpu >= a_need_cpu) and (a_alloc_ram >= a_need_ram)
    b_ok = (b_alloc_cpu >= b_need_cpu) and (b_alloc_ram >= b_need_ram)

    a_cost = cost_for_tick(a_alloc_cpu, a_alloc_ram, price_cpu, price_ram)
    b_cost = cost_for_tick(b_alloc_cpu, b_alloc_ram, price_cpu, price_ram)

    return {
        "minute": t,
        "a_need_cpu": a_need_cpu, "a_need_ram": a_need_ram,
        "b_need_cpu": b_need_cpu, "b_need_ram": b_need_ram,
        "a_alloc_cpu": a_alloc_cpu, "a_alloc_ram": a_alloc_ram,
        "b_alloc_cpu": b_alloc_cpu, "b_alloc_ram": b_alloc_ram,
        "a_sla_ok": int(a_ok), "b_sla_ok": int(b_ok),
        "a_cost": round(a_cost, 6), "b_cost": round(b_cost, 6),
        "cpu_fairness": round(cpu_fairness, 6)
    }
