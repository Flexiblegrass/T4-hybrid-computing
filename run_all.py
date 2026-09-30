# NAMA  : Najmi Sabila Almusfiroh
# NPM   : 247006111125
# KELAS : E

import subprocess, re, sys
print("="*55)
print("NAMA  : Najmi Sabila Almusfiroh")
print("NPM   : 247006111125")
print("KELAS : E")
print("="*55)

LOADERS = [1, 2, 4]
WORKERS = [1, 2, 4, 16]    
QMAX    = [4, 32]

rows = []
for q in QMAX:
    for L in LOADERS:
        for W in WORKERS:
            out = subprocess.run([sys.executable, "hybrid_pipeline.py", str(L), str(W), str(q)],
                                 capture_output=True, text=True).stdout
            total = re.search(r"Total time\s*:\s*([\d.]+)", out).group(1)
            thr   = re.search(r"Throughput\s*:\s*([\d.]+)", out).group(1)
            lat   = re.search(r"Avg latency\s*:\s*([\d.]+)", out).group(1)
            rows.append((L, W, q, total, thr, lat))

print(f"{'Loader':>6} {'Worker':>6} {'Q_MAX':>5} {'Total(s)':>9} {'Thr(file/s)':>12} {'AvgLat(s)':>10}")
for L, W, q, total, thr, lat in rows:
    print(f"{L:>6} {W:>6} {q:>5} {total:>9} {thr:>12} {lat:>10}")

with open("hasil_b1.csv", "w") as f:
    f.write("loader,worker,qmax,total,throughput,latency\n")
    for r in rows:
        f.write(",".join(map(str, r)) + "\n")