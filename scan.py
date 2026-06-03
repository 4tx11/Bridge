#!/usr/bin/env python3
"""
Full TCP port scanner for iSH (Alpine) – scans all 65,535 ports on a target IP.
Usage: python3 full_scan.py
"""

import socket
import threading
import time
from queue import Queue

# ========== CONFIGURATION ==========
TARGET = "162.0.215.160"      # Replace with your target IP
THREADS = 100                 # Number of threads (adjust for iSH performance)
TIMEOUT = 0.5                 # Seconds per connection attempt
# ====================================

def scan_port(port):
    """Test if a port is open by trying a TCP connection."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)
        result = sock.connect_ex((TARGET, port))
        if result == 0:
            print(f"[OPEN] Port {port}")
            with open("open_ports.txt", "a") as f:
                f.write(f"{port}\n")
        sock.close()
    except:
        pass

def worker():
    """Thread worker – pulls ports from queue and scans them."""
    while not queue.empty():
        port = queue.get()
        scan_port(port)
        queue.task_done()

if __name__ == "__main__":
    # Create queue with all 65535 ports
    queue = Queue()
    for port in range(1, 65536):
        queue.put(port)

    print(f"[*] Scanning {TARGET} (all 65535 ports) with {THREADS} threads...")
    start_time = time.time()

    # Start worker threads
    for _ in range(THREADS):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()

    # Wait for all ports to be scanned
    queue.join()

    elapsed = time.time() - start_time
    print(f"[+] Scan completed in {elapsed:.2f} seconds")
    print("[+] Open ports saved to open_ports.txt")
