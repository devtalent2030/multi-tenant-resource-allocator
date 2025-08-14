# =============================================================================
# Project: Multi-Tenant Resource Allocator Simulation
# File: plotting.py
# Author: Talent Nyota
# Date: 2025-08-13
# Description: Generates visualizations comparing resource demand vs allocation 
#              over time, and plots SLA compliance and fairness trends.
# =============================================================================

"""
Plot utilities for the multi-tenant simulation.
Generates PNGs for demand vs allocation and SLA/fairness over time.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def make_plots(csv_path: str) -> None:
    """Create and save plots from a simulation CSV."""
    sns.set_theme(context="talk")

    df = pd.read_csv(csv_path)

    # Tenant A: CPU demand vs allocation
    plt.figure()
    plt.plot(df["minute"], df["a_need_cpu"], label="A CPU need")
    plt.plot(df["minute"], df["a_alloc_cpu"], label="A CPU alloc")
    plt.xlabel("minute"); plt.ylabel("vCPU")
    plt.title("Tenant A CPU")
    plt.legend(); plt.tight_layout()
    plt.savefig("plot_a_cpu.png"); plt.close()

    # Tenant B: CPU demand vs allocation
    plt.figure()
    plt.plot(df["minute"], df["b_need_cpu"], label="B CPU need")
    plt.plot(df["minute"], df["b_alloc_cpu"], label="B CPU alloc")
    plt.xlabel("minute"); plt.ylabel("vCPU")
    plt.title("Tenant B CPU")
    plt.legend(); plt.tight_layout()
    plt.savefig("plot_b_cpu.png"); plt.close()

    # SLA and fairness
    plt.figure()
    plt.plot(df["minute"], df["a_sla_ok"], label="A SLA ok")
    plt.plot(df["minute"], df["b_sla_ok"], label="B SLA ok")
    plt.plot(df["minute"], df["cpu_fairness"], label="CPU fairness (Jain)")
    plt.xlabel("minute"); plt.ylabel("value")
    plt.title("SLA and Fairness over time")
    plt.legend(); plt.tight_layout()
    plt.savefig("plot_sla_fairness.png"); plt.close()

    print("saved: plot_a_cpu.png, plot_b_cpu.png, plot_sla_fairness.png")
