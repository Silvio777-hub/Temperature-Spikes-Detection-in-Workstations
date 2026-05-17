import multiprocessing
import time
import argparse
import os
import numpy as np
import random
import string

def intensive_cpu_compute():
    """Performs heavy matrix multiplication and trigonometric calculations."""
    print(f"[CPU] Process {os.getpid()} initiating High-Intensity Compute...")
    while True:
        # Large matrix multiplication is one of the fastest ways to heat a CPU
        size = 1000
        a = np.random.rand(size, size)
        b = np.random.rand(size, size)
        _ = np.dot(a, b)
        
        # Add some trig for extra heat
        _ = np.sin(a) + np.cos(b)

def aggressive_io_stress():
    """Performs continuous random file writes and deletes to stress Disk and Controller."""
    print(f"[I/O] Process {os.getpid()} initiating Aggressive Disk I/O...")
    filename = f"temp_stress_{os.getpid()}.tmp"
    try:
        while True:
            # Write 100MB of random data
            with open(filename, "wb") as f:
                f.write(os.urandom(100 * 1024 * 1024))
            # Read it back
            with open(filename, "rb") as f:
                _ = f.read()
            os.remove(filename)
    except Exception:
        pass
    finally:
        if os.path.exists(filename):
            os.remove(filename)

def memory_saturation(size_mb):
    """Saturates RAM and performs continuous bit-flipping."""
    print(f"[MEM] Allocating and Saturating {size_mb}MB of RAM...")
    try:
        # Allocate
        data = bytearray(os.urandom(size_mb * 1024 * 1024))
        while True:
            # Bit-flip every 4KB to keep the memory bus active
            for i in range(0, len(data), 4096):
                data[i] = data[i] ^ 0xFF
            time.sleep(0.1)
    except MemoryError:
        print("[MEM] Failed to allocate requested memory.")

def main():
    parser = argparse.ArgumentParser(description="ULTIMATE CPS THERMAL STRESS UTILITY")
    parser.add_argument("--cpu", type=int, default=multiprocessing.cpu_count(), help="Number of CPU cores to saturate")
    parser.add_argument("--io", action="store_true", help="Enable aggressive Disk I/O stress")
    parser.add_argument("--mem", type=int, default=0, help="RAM to saturate in MB")
    parser.add_argument("--duration", type=int, default=60, help="Test duration in seconds")
    
    args = parser.parse_args()
    
    processes = []
    
    print("\n" + "="*50)
    print("      --- ULTIMATE THERMAL STRESS INITIATED ---")
    print("      WARNING: THIS WILL GENERATE SIGNIFICANT HEAT")
    print("="*50)
    print(f"[*] CPU Cores: {args.cpu}")
    print(f"[*] Disk I/O: {'ENABLED' if args.io else 'DISABLED'}")
    print(f"[*] Memory: {args.mem}MB")
    print(f"[*] Duration: {args.duration}s")
    print("="*50 + "\n")
    
    # 1. CPU Saturation
    # Safety Cap: Don't spawn more than 32 processes regardless of input
    safe_cpu_count = min(args.cpu, 32)
    if args.cpu > 32:
        print(f"[!] Warning: Capping stress processes at 32 to prevent OS handle exhaustion.")

    for _ in range(safe_cpu_count):
        p = multiprocessing.Process(target=intensive_cpu_compute)
        p.daemon = True
        p.start()
        time.sleep(0.1) # Staggered start to prevent "Fatal Python error" in streams
        processes.append(p)
        
    # 2. Disk I/O Saturation
    if args.io:
        for _ in range(2): # Dual-stream I/O
            p = multiprocessing.Process(target=aggressive_io_stress)
            p.daemon = True
            p.start()
            processes.append(p)
            
    # 3. RAM Saturation
    if args.mem > 0:
        p = multiprocessing.Process(target=memory_saturation, args=(args.mem,))
        p.daemon = True
        p.start()
        processes.append(p)
        
    try:
        time.sleep(args.duration)
        print("\n[!] Time limit reached.")
    except KeyboardInterrupt:
        print("\n[!] Emergency Stop by User.")
    finally:
        print("[*] Cooling down: Terminating stress processes...")
        for p in processes:
            p.terminate()
            p.join(timeout=1)
            
        # Parent-level disk cleanup: scan and remove leftover temp_stress_*.tmp files
        import glob
        for f in glob.glob("temp_stress_*.tmp"):
            try:
                os.remove(f)
            except Exception:
                pass
                
        print("[*] All stress processes halted.")

if __name__ == "__main__":
    main()
