#!/usr/bin/env python3
import sys, time, os, random
from telethon import TelegramClient, events, Button

# ─── JUST THE VIBE ───────────────────────────────────────────────────────
B = """
\033[1;31m╔══════════════════════════════════════════╗
║        ██████╗ ███████╗██████╗ ███████╗ ║
║        ██╔══██╗██╔════╝██╔══██╗██╔════╝ ║
║        ██║  ██║█████╗  ██║  ██║███████╗ ║
║        ██║  ██║██╔══╝  ██║  ██║╚════██║ ║
║        ██████╔╝███████╗██████╔╝███████║ ║
║        ╚═════╝ ╚══════╝╚═════╝ ╚══════╝ ║
║     ░░░▒▒▒▓▓▓ TERMINAL v1.0 ▓▓▓▒▒▒░░░   ║
╚══════════════════════════════════════════╝\033[0m
"""

TAGS = ["INIT","LOAD","AUTH","SYNC","DECODE","MAP","HOOK","PULSE","SCAN","FETCH"]
MODS = ["kernel.sys","core.bin","cache.map","stream.sock","proxy.io","agent.dl"]
STAT = ["OK","LOADED","READY","ACTIVE","SYNCED"]

def ty(s, sp=0.03):
    for c in s: print(c, end="", flush=True); time.sleep(sp)
    print()

def go():
    os.system("clear" if os.name == "posix" else "cls")
    print(B)
    time.sleep(0.5)
    for _ in range(8):
        t = random.choice(TAGS)
        m = random.choice(MODS)
        st = random.choice(STAT)
        print(f"\033[1;32m[+]\033[0m [{t}] \033[1;33m{m}\033[0m \033[1;32m{st}\033[0m")
        time.sleep(0.07 + random.random() * 0.04)
    for c in "█▓▒░█▓▒░█▓▒░█▓▒░": print(f"\033[1;31m{c}\033[0m", end="", flush=True); time.sleep(0.015)
    print("\n")
    time.sleep(0.3)
    ty("\033[1;36m╔════════════════════════════════════════════╗\033[0m", 0.02)
    ty("\033[1;36m║         TELEGRAM AUTHENTICATION            ║\033[0m", 0.02)
    ty("\033[1;36m╚════════════════════════════════════════════╝\033[0m", 0.02)
    print()
    
    a = input(f"\033[1;32m[→]\033[0m API ID: \033[1;37m")
    print("\033[0m", end="")
    b = input(f"\033[1;32m[→]\033[0m API HASH: \033[1;37m")
    print("\033[0m", end="")
    c = input(f"\033[1;32m[→]\033[0m BOT TOKEN: \033[1;37m")
    print("\033[0m", end="")
    print(f"\n\033[1;33m[+] CONNECTING...\033[0m")
    time.sleep(0.7)
    print(f"\033[1;32m[+] TELEGRAM BRIDGE ACTIVE\033[0m\n")
    return int(a), b, c

def main():
    go()
    aid, ah, tok = None, None, None
    # just the show - no real bot
    ty("\033[1;36m╔════════════════════════════════════════════╗\033[0m", 0.02)
    ty("\033[1;36m║           DEDSEC TERMINAL READY            ║\033[0m", 0.02)
    ty("\033[1;36m╚════════════════════════════════════════════╝\033[0m", 0.02)
    print()
    
    while True:
        try:
            cmd = input("\033[1;31mroot@dedsec:~$\033[0m ").strip()
            if cmd in ["exit","quit"]:
                ty("\033[1;33m[+] TERMINATING...\033[0m")
                for c in "▒░█▓▒░█▓▒░": print(f"\033[1;31m{c}\033[0m",end="",flush=True); time.sleep(0.03)
                print("\n\033[1;32m[+] BYE.\033[0m")
                break
            elif cmd == "":
                continue
            elif cmd == "help":
                ty("\033[1;33mCommands: help, clear, scan, status, exploit, banner, exit\033[0m")
            elif cmd == "clear":
                os.system("clear" if os.name == "posix" else "cls")
                print(B)
            elif cmd == "banner":
                print(B)
            elif cmd == "scan":
                ips = [f"192.168.1.{random.randint(1,254)}" for _ in range(6)]
                ports = [21,22,23,80,443,3306,8080,8443,445,3389]
                ty("\033[1;33m[+] SCANNING TARGETS...\033[0m", 0.02)
                time.sleep(0.3)
                for ip in ips:
                    p_open = random.sample(ports, random.randint(2,5))
                    svcs = ["HTTP","SSH","FTP","HTTPS","MySQL","RDP","SMB","Telnet"]
                    print(f"\033[1;32m[+]\033[0m {ip} → ", end="")
                    for p in p_open:
                        svc = random.choice(svcs)
                        print(f"\033[1;33m{p}/{svc}\033[0m", end=" ")
                    print()
                    time.sleep(0.1 + random.random() * 0.1)
                print(f"\033[1;32m[+] {len(ips)} hosts found\033[0m")
            elif cmd == "status":
                ty("\033[1;32m[+] SYSTEM STATUS\033[0m", 0.02)
                items = [
                    ("KERNEL","ACTIVE","\033[1;32m"),
                    ("CORE","ONLINE","\033[1;32m"),
                    ("PROXY","STANDBY","\033[1;33m"),
                    ("TUNNEL","ESTABLISHED","\033[1;32m"),
                    ("AGENT","DEPLOYED","\033[1;32m"),
                    ("ENCRYPTION","AES-256","\033[1;34m"),
                ]
                for name, val, col in items:
                    print(f"  \033[1;30m├\033[0m {name}: {col}{val}\033[0m")
                    time.sleep(0.08)
                print(f"  \033[1;30m└\033[0m UPTIME: \033[1;34m{random.randint(1,999)}h {random.randint(0,59)}m\033[0m")
            elif cmd == "exploit":
                ty("\033[1;33m[+] SELECTING PAYLOAD...\033[0m", 0.02)
                time.sleep(0.3)
                payloads = [
                    "reverse_tcp/x64/shell",
                    "meterpreter/reverse_https",
                    "web_delivery/script",
                    "bind_tcp/stageless",
                    "cmd_exec/powershell",
                ]
                targets = ["192.168.1." + str(random.randint(100,254)) for _ in range(3)]
                p = random.choice(payloads)
                print(f"\033[1;32m[+]\033[0m Payload: \033[1;33m{p}\033[0m")
                print(f"\033[1;32m[+]\033[0m Target: \033[1;33m{random.choice(targets)}:{random.choice([4444,5555,7777,8888])}\033[0m")
                time.sleep(0.5)
                print(f"\033[1;32m[+]\033[0m Generating shellcode...")
                for c in "▓▒░▓▒░▓▒░▓▒░": print(f"\033[1;31m{c}\033[0m",end="",flush=True); time.sleep(0.03)
                print(f"\n\033[1;32m[+]\033[0m Shellcode: \033[1;33m{os.urandom(4).hex()}...{os.urandom(4).hex()}\033[0m")
                print(f"\033[1;32m[+]\033[0m Payload ready. Press enter to deploy or type 'cancel'")
                r = input()
                if r == "cancel":
                    ty("\033[1;33m[+] ABORTED.\033[0m")
                else:
                    ty("\033[1;31m[+] PAYLOAD DEPLOYED\033[0m")
                    time.sleep(0.3)
                    ty("\033[1;32m[+] Session opened\033[0m")
            else:
                ty(f"\033[1;31m[-] Unknown: {cmd}\033[0m")
        except KeyboardInterrupt:
            print()
            ty("\033[1;33m[+] INTERRUPT\033[0m")
            break
        except Exception as e:
            ty(f"\033[1;31m[-] Error: {e}\033[0m")

if __name__ == "__main__":
    main()
