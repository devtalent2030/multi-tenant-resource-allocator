# =============================================================================
# Project: Multi-Tenant Resource Allocator Simulation
# File: workloads.py
# Author: Talent Nyota
# Date: 2025-08-13
# Description: Defines workload demand generation for different tenant types, 
#              including a flash-sale e-commerce spike and a batch job workload.
# =============================================================================

"""
Workload generators for two tenants in the simulation.

Tenant A: flash-sale e-commerce burst (short spike).
Tenant B: batch analytics job (steady window).
"""

import numpy as np
import random

# fixed RNG for reproducible runs
_rng = np.random.default_rng(42)

def _clip_pos(x):
    """Return a non-negative integer from a numeric value."""
    return int(x) if x > 0 else 0

def tenant_a_demand(t):
    """
    Per-minute demand for Tenant A (CPU, RAM).
    Flash sale from minute 30 to 44 increases usage.
    """
    if 30 <= t < 45:
        cpu = _clip_pos(_rng.normal(24, 3))
        ram = _clip_pos(_rng.normal(16, 2))
    else:
        cpu = _clip_pos(_rng.normal(10, 2))
        ram = _clip_pos(_rng.normal(8, 1.5))

    # small integer jitter to avoid perfectly smooth traces
    cpu += random.choice([0, 0, 1, -1])
    ram += random.choice([0, 0, 1, -1])

    return max(cpu, 0), max(ram, 0)

def tenant_b_demand(t):
    """
    Per-minute demand for Tenant B (CPU, RAM).
    Batch job runs from minute 60 to 119 with steady usage.
    """
    if 60 <= t < 120:
        cpu = _clip_pos(_rng.normal(13, 1.5))
        ram = _clip_pos(_rng.normal(12, 1.5))
    else:
        cpu, ram = 0, 0
    return cpu, ram
