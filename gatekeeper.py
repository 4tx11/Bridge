import os, requests, random, time, sys
from concurrent.futures import ThreadPoolExecutor

# --- [ STEP 1: LOCAL INJECTION ] ---
# This part stays blank on GitHub. You fill it in on your iPad.
os.system('clear')
print("\033[35m[!] SHADOW PROTOCOL: SECURE LOGIN\033[0m")
TOKEN = input("\033[32m[?] Enter Bot Token: \033[0m")
CHAT_ID = input("\033[32m[?] Enter Chat ID: \033[0m")
RAW_COOKIES = input("\033[32m[?] Paste FB Cookies: \033[0m")

# --- [ STEP 2: CORE LOGIC ] ---
P, B, G, R, W = "\033[35m", "\033[34m", "\033[32m", "\033[31m", "\033[0m"

def parse_cookies(ck):
    return {i.split('=')[0].strip(): i.split('=')[1] for i in ck.split(';') if '=' in i}

class ShadowTool:
    def __init__(self):
        self.loop, self.oks, self.ids = 0, [], []
        self.session = requests.Session()
        self.session.cookies.update(parse_cookies(RAW_COOKIES))

    def check_auth(self):
        try:
            r = self.session.get("https://mbasic.facebook.com/profile.php", timeout=10)
            if "Log Out" in r.text:
                print(f"{G}[+] AUTH SUCCESSFUL\033[0m")
                return True
            print(f"{R}[x] AUTH FAILED\033[0m"); return False
        except: return False

    def report(self, uid):
        text = f"🔮 *HIT FOUND*\nID: `{uid}`\n⚡ _Shadow v3.5_"
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"})

    def hunt(self, uid):
        sys.stdout.write(f"\r{B}[ SCANNING ] {W}{self.loop} | {G}HITS: {len(self.oks)}{W}")
        sys.stdout.flush()
        try:
            r = self.session.get(f"https://mbasic.facebook.com/{uid}", timeout=10)
            if "Add Friend" in r.text and "0 posts" in r.text.lower():
                self.oks.append(uid); self.report(uid)
        except: pass
        self.loop += 1

    def run(self):
        if not self.check_auth(): return
        limit = int(input(f"\n{P}[?] Scan Depth: {W}"))
        for _ in range(limit):
            self.ids.append("100003" + str(random.randint(111111111, 999999999)))
        with ThreadPoolExecutor(max_workers=20) as ex:
            ex.map(self.hunt, self.ids)

if __name__ == "__main__":
    ShadowTool().run()
