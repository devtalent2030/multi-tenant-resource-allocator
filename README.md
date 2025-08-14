# Multi-Tenant Resource Allocator

A Python-based simulation that models a **multi-tenant cloud environment** and dynamically allocates compute resources (CPU, memory, storage) based on **real-time demand**.

This project simulates multiple workloads — such as **e-commerce flash sales** and **batch analytics jobs** — sharing the same cloud infrastructure. The allocation algorithm balances **performance, cost efficiency, and fairness**, while meeting service-level agreements (SLAs).

## 📌 Key Features
- **Dynamic Workload Simulation** – Models realistic demand patterns with bursts and scheduled jobs.
- **SLA-Aware Allocation** – Ensures critical workloads meet performance targets.
- **Fair Resource Sharing** – Weighted allocation when demand exceeds capacity.
- **Cost Tracking** – Calculates CPU/RAM usage costs based on defined pricing.
- **Visualization** – Generates usage and allocation graphs with Matplotlib.

## 🏗 Project Structure
```

multi-tenant-resource-allocator/
│
├── simulate.py          # Main simulation loop
├── workloads.py         # Workload demand generation
├── allocator.py         # Allocation algorithm
├── metrics.py           # SLA, cost, and fairness calculations
├── plotting.py          # Matplotlib visualizations
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation

````

## ⚙️ Tech Stack
- **Python 3.9+**
- [NumPy](https://numpy.org/) – numerical computation
- [Pandas](https://pandas.pydata.org/) – data handling
- [Matplotlib](https://matplotlib.org/) / [Seaborn](https://seaborn.pydata.org/) – visualization
- [Logging](https://docs.python.org/3/library/logging.html) – trace allocation decisions

## 📊 Example Use Case
- **Tenant A**: E-commerce platform experiencing a 15-min flash sale with high traffic.
- **Tenant B**: Nightly analytics job requiring high sustained CPU/RAM for a fixed window.

The simulation demonstrates how a cloud operator can maintain SLAs for both tenants under shared capacity, while minimizing operational costs.

## 🚀 Getting Started
### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/multi-tenant-resource-allocator.git
cd multi-tenant-resource-allocator
````

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the simulation

```bash
python simulate.py
```

### 4. View results

* **CSV log** of allocations and SLA breaches
* **Graphs** showing demand, allocation, cost trends

## 🧠 Learning Outcomes

This project demonstrates:

* Cloud fundamentals: **elasticity**, **multi-tenancy**, **resource pooling**
* SLA-driven system design
* Algorithm development for fairness & optimization
* Visualization and data analysis in Python

## 📄 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

