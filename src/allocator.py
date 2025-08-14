# =============================================================================
# Project: Multi-Tenant Resource Allocator Simulation
# File: allocator.py
# Author: Talent Nyota
# Date: 2025-08-13
# Description: Implements the allocation algorithm for distributing CPU and RAM 
#              between multiple tenants based on demand, floors, and weights.
# =============================================================================

"""
Resource allocation functions for a multi-tenant simulation.
Implements a simple fair-share model with floors and weighted surplus split.
"""

def allocate(a_need, b_need, total_cpu, total_ram, floors, weights):
    """
    Allocate CPU and RAM between two tenants based on demand, floors, and weights.

    Args:
        a_need (tuple): (CPU_demand, RAM_demand) for tenant A.
        b_need (tuple): (CPU_demand, RAM_demand) for tenant B.
        total_cpu (int): Total available vCPUs.
        total_ram (int): Total available RAM in GB.
        floors (tuple): Minimum CPU and RAM guarantees for both tenants
                        (A_CPU_floor, A_RAM_floor, B_CPU_floor, B_RAM_floor).
        weights (tuple): Relative priority weights for A and B.

    Returns:
        dict: Final allocated CPU and RAM for both tenants.
    """
    a_need_cpu, a_need_ram = a_need
    b_need_cpu, b_need_ram = b_need
    a_floor_cpu, a_floor_ram, b_floor_cpu, b_floor_ram = floors
    a_w, b_w = weights

    # ---- CPU allocation ----
    a_cpu = min(a_need_cpu, a_floor_cpu)
    b_cpu = min(b_need_cpu, b_floor_cpu)

    # If floors alone exceed total capacity, trim from B first, then A
    if a_cpu + b_cpu > total_cpu:
        over = (a_cpu + b_cpu) - total_cpu
        trim = min(over, b_cpu)
        b_cpu -= trim
        over -= trim
        if over > 0:
            a_cpu -= min(over, a_cpu)

    cpu_left = max(0, total_cpu - (a_cpu + b_cpu))
    a_gap = max(0, a_need_cpu - a_cpu)
    b_gap = max(0, b_need_cpu - b_cpu)

    if cpu_left > 0 and (a_gap + b_gap) > 0:
        total_w = (a_w + b_w) if (a_w + b_w) > 0 else 1.0
        give_a = int(cpu_left * (a_w / total_w))
        give_b = cpu_left - give_a

        a_cpu += min(give_a, a_gap)
        b_cpu += min(give_b, b_gap)

        leftover = max(0, total_cpu - (a_cpu + b_cpu))

        # If rounding gave nothing, give 1 to A if needed
        if leftover > 0 and give_a == 0 and give_b == 0:
            if a_cpu < a_need_cpu:
                a_cpu += 1
                leftover -= 1

        # Distribute any final leftovers
        if leftover > 0 and a_cpu < a_need_cpu:
            take = min(leftover, a_need_cpu - a_cpu)
            a_cpu += take
            leftover -= take
        if leftover > 0 and b_cpu < b_need_cpu:
            b_cpu += min(leftover, b_need_cpu - b_cpu)

    # ---- RAM allocation ----
    a_ram = min(a_need_ram, a_floor_ram)
    b_ram = min(b_need_ram, b_floor_ram)

    if a_ram + b_ram > total_ram:
        over = (a_ram + b_ram) - total_ram
        trim = min(over, b_ram)
        b_ram -= trim
        over -= trim
        if over > 0:
            a_ram -= min(over, a_ram)

    ram_left = max(0, total_ram - (a_ram + b_ram))
    a_gap = max(0, a_need_ram - a_ram)
    b_gap = max(0, b_need_ram - b_ram)

    if ram_left > 0 and (a_gap + b_gap) > 0:
        total_w = (a_w + b_w) if (a_w + b_w) > 0 else 1.0
        give_a = int(ram_left * (a_w / total_w))
        give_b = ram_left - give_a

        a_ram += min(give_a, a_gap)
        b_ram += min(give_b, b_gap)

        leftover = max(0, total_ram - (a_ram + b_ram))

        if leftover > 0 and give_a == 0 and give_b == 0:
            if a_ram < a_need_ram:
                a_ram += 1
                leftover -= 1

        if leftover > 0 and a_ram < a_need_ram:
            take = min(leftover, a_need_ram - a_ram)
            a_ram += take
            leftover -= take
        if leftover > 0 and b_ram < b_need_ram:
            b_ram += min(leftover, b_need_ram - b_ram)

    return {"a_cpu": a_cpu, "a_ram": a_ram, "b_cpu": b_cpu, "b_ram": b_ram}
