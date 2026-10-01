# NAMA  : Najmi Sabila Almusfiroh
# NPM   : 247006111125
# KELAS : E
# FILE MODIFIKASI DARI KODE SLIDE 20 (Praktikum 2 - MPI + ProcessPool, Monte Carlo pi)
# Parameter A = 5 (digit terakhir NPM) -> SAMPLES_PER_TASK = 200000 + 10000*5 = 250000
# Bagian yang diubah/ditambahkan dari kode asli slide ditandai "[UBAH]".

# [UBAH] Perbaikan untuk Windows/MS-MPI: matikan auto-inisialisasi MPI saat import,
#        agar proses anak yang di-spawn ProcessPool tidak ikut meng-init MPI
#        (kalau tidak, muncul error "failed to attach to a bootstrap queue").
import mpi4py
mpi4py.rc.initialize = False
mpi4py.rc.finalize = False
from mpi4py import MPI
from concurrent.futures import ProcessPoolExecutor
import numpy as np, time, sys

def mc_pi(n_samples, seed):
    rng = np.random.default_rng(seed)
    x = rng.random(n_samples); y = rng.random(n_samples)
    inside = (x*x + y*y) <= 1.0
    return int(inside.sum())

# [UBAH] PERBAIKAN BUG UTAMA:
#        Kode asli slide memakai lambda di ex.map(), padahal ProcessPoolExecutor
#        harus mem-"pickle" fungsi untuk dikirim ke proses lain, dan lambda TIDAK
#        bisa di-pickle -> PicklingError. Solusi: ganti lambda dengan fungsi biasa
#        di level modul (run_task) yang bisa di-pickle.
def run_task(args):
    k, samples, seed_base = args
    return mc_pi(samples, seed_base + k)

def chunk_range(total, parts, idx):
    base = total // parts; rem = total % parts
    start = idx * base + min(idx, rem)
    end = start + base + (1 if idx < rem else 0)
    return start, end

if __name__ == "__main__":
    MPI.Init()                     # [UBAH] inisialisasi MPI hanya di proses utama
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    TOTAL_TASKS = 8
    SAMPLES_PER_TASK = 200_000 + 10_000 * 5    # [UBAH] A = 5 -> 250_000 (asli slide: 250_000 tetap)
    WORKERS = int(sys.argv[1]) if len(sys.argv) > 1 else 4   # [UBAH] jumlah worker via argumen

    start, end = chunk_range(TOTAL_TASKS, size, rank)
    my_tasks = range(start, end)

    t0 = time.time()
    with ProcessPoolExecutor(max_workers=WORKERS) as ex:
        # [UBAH] kirim argumen sebagai daftar tuple + pakai run_task (bukan lambda)
        args = [(k, SAMPLES_PER_TASK, 1234 + rank * 1000) for k in my_tasks]
        hits = list(ex.map(run_task, args))
    local_hits = sum(hits)
    local_samples = len(my_tasks) * SAMPLES_PER_TASK
    t1 = time.time()

    global_hits = comm.reduce(local_hits, op=MPI.SUM, root=0)
    global_samp = comm.reduce(local_samples, op=MPI.SUM, root=0)
    makespan = comm.reduce(t1 - t0, op=MPI.MAX, root=0)

    if rank == 0:
        # [UBAH] cetak identitas (bukti kepemilikan) di rank 0
        print("="*55)
        print("NAMA  : Najmi Sabila Almusfiroh")
        print("NPM   : 247006111125")
        print("KELAS : E")
        print("="*55)
        pi_est = 4.0 * global_hits / global_samp
        print(f"[MPI ranks={size}] tasks={TOTAL_TASKS}, per_task={SAMPLES_PER_TASK}, workers={WORKERS}")
        print(f"Makespan     : {makespan:.3f} s")
        print(f"Total samples : {global_samp:,}")
        print(f"Estimasi pi   : {pi_est:.6f}")
    MPI.Finalize()                 # [UBAH] tutup MPI secara eksplisit