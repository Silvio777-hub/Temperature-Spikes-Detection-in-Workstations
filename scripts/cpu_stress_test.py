import multiprocessing as mp
import time
import os
import argparse

def _worker(ev):
    """Busy loop to maximize CPU usage."""
    while not ev.is_set():
        # Mathematical computation to keep the core busy
        _ = [x**2 for x in range(1000)]

def run_stress(duration, core_count=None):
    if core_count is None:
        core_count = os.cpu_count() or 1
        
    print(f"Starting CPU stress on {core_count} cores for {duration} seconds...")
    stop_event = mp.Event()
    processes = []
    
    for _ in range(core_count):
        p = mp.Process(target=_worker, args=(stop_event,))
        p.start()
        processes.append(p)
        
    time.sleep(duration)
    stop_event.set()
    
    for p in processes:
        p.join()
    print("Stress test complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Thermal Stressor")
    parser.add_argument("--duration", type=int, default=60, help="Stress duration in seconds")
    parser.add_argument("--cores", type=int, default=None, help="Number of cores to stress")
    args = parser.parse_args()
    
    run_stress(args.duration, args.cores)
