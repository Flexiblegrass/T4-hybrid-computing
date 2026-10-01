# NAMA  : Najmi Sabila Almusfiroh
# NPM   : 247006111125
# KELAS : E
# Membuat dataset 150 file .txt
# Berdasarkan skrip "Cara RUN" pada slide 19. Jumlah file = 100 + 10*A,
# dengan A = 5 (digit terakhir NPM) sehingga menghasilkan 150 file.

import os, random, string, pathlib
pathlib.Path("data").mkdir(exist_ok=True)
JUMLAH = 100 + 10 * 5    # = 150  (A = 5)
for i in range(1, JUMLAH + 1):
    
    # isi file: karakter acak sepanjang 3000 karakter
    s = "".join(random.choice(string.ascii_letters + " " * 5 + "\n") for _ in range(3000))
    open(f"data/file_{i:03d}.txt", "w").write(s)
print(f"done. {JUMLAH} file dibuat di folder ./data")