# NAMA  : Najmi Sabila Almusfiroh
# NPM   : 247006111125
# KELAS : E

import os, random, string, pathlib
pathlib.Path("data").mkdir(exist_ok=True)
JUMLAH = 100 + 10 * 5    # = 150
for i in range(1, JUMLAH + 1):
    s = "".join(random.choice(string.ascii_letters + " " * 5 + "\n") for _ in range(3000))
    open(f"data/file_{i:03d}.txt", "w").write(s)
print(f"done. {JUMLAH} file dibuat di folder ./data")