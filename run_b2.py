# NAMA  : Najmi Sabila Almusfiroh
# NPM   : 247006111125
# KELAS : E
# Menjalankan mpi_hybrid_processpool.py untuk 9 kombinasi
# (rank MPI x worker) secara otomatis, lalu menghitung Speedup & Efisiensi
# dan mencetaknya dalam bentuk tabel.

import subprocess, re, sys

print("="*60)
print("NAMA  : Najmi Sabila Almusfiroh")
print("NPM   : 247006111125")
print("KELAS : E")
print("="*60)

RANKS   = [1, 2, 4]
WORKERS = [1, 2, 4]

hasil = {}
for r in RANKS:
    for w in WORKERS:
        out = subprocess.run(
            ["mpiexec", "-n", str(r), sys.executable, "mpi_hybrid_processpool.py", str(w)],
            capture_output=True, text=True).stdout
        m = re.search(r"Makespan\s*:\s*([\d.]+)", out)
        hasil[(r, w)] = float(m.group(1)) if m else None

T1 = hasil[(1, 1)]   # baseline: 1 rank x 1 worker

print(f"\n{'Rank':>5}{'Worker':>8}{'n':>5}{'Makespan(s)':>13}{'Speedup':>10}{'Efisiensi':>11}")
for r in RANKS:
    for w in WORKERS:
        t = hasil[(r, w)]; n = r * w
        S = T1 / t; E = S / n
        print(f"{r:>5}{w:>8}{n:>5}{t:>13.3f}{S:>10.2f}{E:>11.2f}")