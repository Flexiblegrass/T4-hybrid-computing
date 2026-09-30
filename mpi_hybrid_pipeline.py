# NAMA  : Najmi Sabila Almusfiroh
# NPM   : 247006111125
# KELAS : E

from mpi4py import MPI
from concurrent.futures import ProcessPoolExecutor
import numpy as np, time, sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def mc_pi(n_samples, seed):
    rng = np.random.default_rng(seed)
    x = rng.random(n_samples); y = rng.random(n_samples)
    inside = (x*x + y*y) <= 1.0
    return int(inside.sum())

def run_task(args):
    k, samples, seed_base = args
    return mc_pi(samples, seed_base + k)

def chunk_range(total, parts, idx):
    base = total // parts; rem = total % parts
    start = idx * base + min(idx, rem)
    end = start + base + (1 if idx < rem else 0)
    return start, end

if __name__ == "__main__":
    TOTAL_TASKS = 8
    SAMPLES_PER_TASK = 200_000 + 10_000 * 5   

    WORKERS = int(sys.argv[1]) if len(sys.argv) > 1 else 4

    start, end = chunk_range(TOTAL_TASKS, size, rank)
    my_tasks = range(start, end)

    t0 = time.time()
    with ProcessPoolExecutor(max_workers=WORKERS) as ex:
 
        args = [(k, SAMPLES_PER_TASK, 1234 + rank * 1000) for k in my_tasks]
        hits = list(ex.map(run_task, args))
    local_hits = sum(hits)
    local_samples = len(my_tasks) * SAMPLES_PER_TASK
    t1 = time.time()

    global_hits = comm.reduce(local_hits, op=MPI.SUM, root=0)
    global_samp = comm.reduce(local_samples, op=MPI.SUM, root=0)
    makespan = comm.reduce(t1 - t0, op=MPI.MAX, root=0)

    if rank == 0:
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