# src/stress_test.py
"""
Stress Test Script
-------------------
A lightweight pure‑Python stress utility that can generate CPU and GPU load for a configurable duration.
It is intended for demonstration purposes in the Temperature Spikes Detection project.

Usage examples:
    python -m src.stress_test --duration 120 --cpu 4       # 4 CPU workers for 2 minutes
    python -m src.stress_test --duration 60  --gpu 1       # 1 GPU worker for 1 minute
    python -m src.stress_test --duration 180 --cpu 8 --gpu 2

The script:
    * Spawns ``cpu`` worker threads that perform endless NumPy matrix multiplications.
    * Optionally spawns ``gpu`` workers that perform GPU‑bound matrix multiplications using ``py3nvml`` to locate a device.
    * Runs for ``duration`` seconds and then gracefully terminates all workers.
"""

import argparse
import threading
import time
import numpy as np
import sys

# Optional GPU support – imported lazily to avoid hard dependency on systems without a GPU.
try:
    import py3nvml.py3nvml as nvml
    _GPU_AVAILABLE = True
except Exception:
    _GPU_AVAILABLE = False


def cpu_worker(stop_event: threading.Event, worker_id: int) -> None:
    """Continuously multiply two random matrices until stopped.

    Args:
        stop_event: threading.Event used to signal termination.
        worker_id: Identifier for debugging output.
    """
    # Small 256×256 matrices keep memory usage modest while still providing significant load.
    a = np.random.rand(256, 256)
    b = np.random.rand(256, 256)
    while not stop_event.is_set():
        # The result is deliberately discarded – we only care about CPU cycles.
        np.dot(a, b)
    # Optional debug print – comment out for silent operation.
    # print(f"CPU worker {worker_id} terminated")


def gpu_worker(stop_event: threading.Event, device_index: int) -> None:
    """Perform simple GPU arithmetic using the NVIDIA Management Library.

    This does **not** require CUDA but forces the GPU to stay active by
    repeatedly reading/writing device counters.
    """
    if not _GPU_AVAILABLE:
        print("GPU support not available on this system.")
        return
    nvml.nvmlInit()
    handle = nvml.nvmlDeviceGetHandleByIndex(device_index)
    while not stop_event.is_set():
        # Query a few counters – this keeps the GPU busy enough for our demo.
        nvml.nvmlDeviceGetUtilizationRates(handle)
        time.sleep(0.01)  # tiny sleep prevents a tight busy‑wait loop.
    nvml.nvmlShutdown()
    # print(f"GPU worker {device_index} terminated")


def run_stress(duration: int, cpu_workers: int, gpu_workers: int) -> None:
    stop_event = threading.Event()
    threads = []
    # Launch CPU workers
    for i in range(cpu_workers):
        t = threading.Thread(target=cpu_worker, args=(stop_event, i), daemon=True)
        t.start()
        threads.append(t)
    # Launch GPU workers if requested and available
    if gpu_workers > 0:
        if not _GPU_AVAILABLE:
            print("Warning: py3nvml not installed or no NVIDIA GPU detected – GPU workers will be skipped.")
        else:
            device_count = nvml.nvmlDeviceGetCount()
            for i in range(min(gpu_workers, device_count)):
                t = threading.Thread(target=gpu_worker, args=(stop_event, i), daemon=True)
                t.start()
                threads.append(t)
    print(f"[Stress] Running for {duration}s – CPU workers: {cpu_workers}, GPU workers: {gpu_workers}")
    try:
        time.sleep(duration)
    except KeyboardInterrupt:
        print("[Stress] Interrupted by user")
    finally:
        stop_event.set()
        # Give a brief moment for threads to exit cleanly.
        for t in threads:
            t.join(timeout=1.0)
        print("[Stress] Completed.")


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="CPU/GPU stress test for Temperature‑Spikes project")
    parser.add_argument("--duration", type=int, default=60,
                        help="How many seconds to run the stress test (default: 60)")
    parser.add_argument("--cpu", type=int, default=4,
                        help="Number of parallel CPU workers (default: 4)")
    parser.add_argument("--gpu", type=int, default=0,
                        help="Number of GPU workers (requires NVIDIA GPU and py3nvml) (default: 0)")
    return parser.parse_args(argv)


if __name__ == "__main__":
    args = parse_args()
    # Clamp values to sensible ranges.
    cpu = max(1, args.cpu)
    gpu = max(0, args.gpu)
    duration = max(10, args.duration)
    run_stress(duration, cpu, gpu)
