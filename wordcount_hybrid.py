# NAMA  : Najmi Sabila Almusfiroh
# NPM   : 247006111125
# KELAS : E

from mpi4py import MPI
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from collections import Counter
import os, re, time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

DATA_DIR = "./data_wc"
N_WORKERS = 4
STOPWORDS = {"dan", "yang", "di", "the", "of", "and"} 
def count_file(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        txt = f.read().lower()
    words = re.findall(r"[a-z0-9]+", txt)      
    return Counter(words)

def chunk_range(total, parts, idx):
    base = total // parts; rem = total % parts
    start = idx * base + min(idx, rem)
    end = start + base + (1 if idx < rem else 0)
    return start, end

def proses(my_files, mode):

    t0 = time.time()
    local = Counter()
    Pool = ThreadPoolExecutor if mode == "threads" else ProcessPoolExecutor
    with Pool(max_workers=N_WORKERS) as ex:
        for c in ex.map(count_file, my_files):
            local += c
    return local, time.time() - t0

if __name__ == "__main__":

    all_files = None
    if rank == 0:
        all_files = sorted(os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR)
                           if f.endswith(".txt"))
    all_files = comm.bcast(all_files, root=0)

    start, end = chunk_range(len(all_files), size, rank)
    my_files = all_files[start:end]

    local_t, time_threads = proses(my_files, "threads")

    local_p, time_proc = proses(my_files, "processes")

    gathered = comm.gather(local_t, root=0)
    gt = comm.reduce(time_threads, op=MPI.MAX, root=0)   
    gp = comm.reduce(time_proc,    op=MPI.MAX, root=0)

    if rank == 0:
        print("="*55)
        print("NAMA  : Najmi Sabila Almusfiroh")
        print("NPM   : 247006111125")
        print("KELAS : E")
        print("="*55)
        global_counter = Counter()
        for c in gathered:
            global_counter += c

        for sw in STOPWORDS:
            global_counter.pop(sw, None)

        print(f"[MPI ranks={size}] files={len(all_files)} | workers/rank={N_WORKERS}")
        print(f"Waktu versi ThreadPool  : {gt:.4f} s")
        print(f"Waktu versi ProcessPool : {gp:.4f} s")
        lebih = "ThreadPool" if gt < gp else "ProcessPool"
        print(f"Lebih cepat: {lebih}")
        print("\n10 kata teratas (setelah stopwords dibuang):")
        for w, c in global_counter.most_common(10):
            print(f"  {w:>12} : {c}")