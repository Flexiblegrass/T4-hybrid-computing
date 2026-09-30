# NAMA  : Najmi Sabila Almusfiroh
# NPM   : 247006111125
# KELAS : E

import os, sys, time, threading, queue, string
from concurrent.futures import ProcessPoolExecutor, as_completed

DATA_DIR = "./data"                                 

N_LOADER_THREADS = int(sys.argv[1]) if len(sys.argv) > 1 else 2   
N_WORKERS        = int(sys.argv[2]) if len(sys.argv) > 2 else 4  
Q_MAX            = int(sys.argv[3]) if len(sys.argv) > 3 else 32  

def cpu_task(path):
    t0 = time.time()
    with open(path, "rb") as f:
        data = f.read()
    text = data.decode(errors="ignore").lower()
    alpha = sum(c in string.ascii_lowercase for c in text) 
    latency = time.time() - t0
    return {"path": path, "alpha": alpha, "latency": latency}

def loader_worker(q, files):
    for p in files:
        q.put(p)           
    q.put(None)             

def run_pipeline():
    files = [os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR)
             if os.path.isfile(os.path.join(DATA_DIR, f))]
    if not files:
        raise SystemExit("Folder ./data kosong - siapkan beberapa .txt dulu.")

    chunks = [files[i::N_LOADER_THREADS] for i in range(N_LOADER_THREADS)]
    q = queue.Queue(maxsize=Q_MAX)

    loaders = []
    for ch in chunks:
        t = threading.Thread(target=loader_worker, args=(q, ch)); t.start()
        loaders.append(t)

    done = 0
    results, lat = [], []
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=N_WORKERS) as ex:
        futs = set()
        while done < N_LOADER_THREADS:
            item = q.get()          
            if item is None:
                done += 1; continue
            futs.add(ex.submit(cpu_task, item))
        for fut in as_completed(futs):
            r = fut.result()
            results.append(r); lat.append(r["latency"])

    total = time.time() - t0
    thr = len(results) / total if total > 0 else 0.0
    avg_lat = sum(lat) / len(lat) if lat else 0.0

    print(f"Files            : {len(results)}")
    print(f"Threads (I/O)    : {N_LOADER_THREADS} | Processes (CPU): {N_WORKERS} | Q_MAX: {Q_MAX}")
    print(f"Total time       : {total:.3f} s")
    print(f"Throughput       : {thr:.2f} files/s")
    print(f"Avg latency      : {avg_lat:.4f} s/file")

if __name__ == "__main__":
    run_pipeline()