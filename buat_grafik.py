# NAMA  : Najmi Sabila Almusfiroh
# NPM   : 247006111125
# KELAS : E

import csv, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
print("="*55)
print("NAMA  : Najmi Sabila Almusfiroh")
print("NPM   : 247006111125")
print("KELAS : E")
print("="*55)

data = list(csv.DictReader(open("hasil_b1.csv")))
loaders = sorted(set(int(r["loader"]) for r in data))
qmaxs   = sorted(set(int(r["qmax"]) for r in data))

fig, axes = plt.subplots(1, len(qmaxs), figsize=(12, 5), sharey=True)
for ax, q in zip(axes, qmaxs):
    for L in loaders:
        pts = sorted([(int(r["worker"]), float(r["throughput"]))
                      for r in data if int(r["qmax"]) == q and int(r["loader"]) == L])
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        ax.plot(xs, ys, marker="o", label=f"{L} loader thread")
    ax.set_title(f"Q_MAX = {q}")
    ax.set_xlabel("N_WORKERS (jumlah proses)")
    ax.set_xticks([1, 2, 4, 16])
    ax.grid(True, alpha=0.3)
    ax.legend()
axes[0].set_ylabel("Throughput (file/detik)")
fig.suptitle("B1 - Throughput vs N_WORKERS (Najmi Sabila A. / 247006111125)", fontweight="bold")
fig.tight_layout()
fig.savefig("grafik_b1.png", dpi=130, bbox_inches="tight")
print("grafik_b1.png dibuat")