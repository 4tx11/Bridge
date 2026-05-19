#!/usr/bin/env python3
import sys, time, os, random, requests, json
from urllib.parse import quote_plus
from telethon import TelegramClient, events, Button

B = """
\033[1;31m╔══════════════════════════════════════════╗
║        ██████╗ ███████╗██████╗ ███████╗ ║
║        ██╔══██╗██╔════╝██╔══██╗██╔════╝ ║
║        ██║  ██║█████╗  ██║  ██║███████╗ ║
║        ██║  ██║██╔══╝  ██║  ██║╚════██║ ║
║        ██████╔╝███████╗██████╔╝███████║ ║
║        ╚═════╝ ╚══════╝╚═════╝ ╚══════╝ ║
║     ░░░▒▒▒▓▓▓ HUNTER v1.0 ▓▓▓▒▒▒░░░     ║
╚══════════════════════════════════════════╝\033[0m
"""

CATS = {
    "🎮 Game Hacks": [
        "pubg hack", "fortnite cheat", "valorant aimbot", "game hack tool",
        "pubg esp wallhack", "fortnite aimbot undetected", "game cheating bypass"
    ],
    "🔓 Account Dumps": [
        "combo list email password", "account dump leak", "credential dump",
        "database leak accounts", "combo list 2025"
    ],
    "🤖 AI Hacking": [
        "ai jailbreak prompt", "chatgpt system prompt leak", "llm exploitation",
        "ai red team tool", "prompt injection hack"
    ],
    "🐍 Python Tools": [
        "python reverse shell", "python keylogger", "python brute force",
        "python scraper osint", "python exploit code"
    ],
    "🌐 Social Media": [
        "instagram hack python", "telegram scraper", "discord token generator",
        "facebook account cracker", "instagram brute force"
    ],
    "🛠️ Hacking Tools": [
        "sql injection tool", "xss payload generator", "reverse shell one liner",
        "privilege escalation script", "web shell upload"
    ],
    "💀 Malware": [
        "remote access trojan python", "info stealer source code",
        "keylogger download", "rat builder"
    ],
    "🌑 Altenen": [
        "site:altenens.is hack tool", "site:altenens.is account dump",
        "site:altenens.is cheat", "site:altenens.com hack"
    ],
    "📦 GitHub": [
        "github.com pubg cheat", "github.com account checker",
        "github.com reverse shell", "github.com instagram hack"
    ],
}

TAGS = ["INIT","LOAD","AUTH","SYNC","DECODE","MAP","HOOK","PULSE","SCAN"]
MODS = ["kernel.sys","core.bin","cache.map","stream.sock","proxy.io"]
STAT = ["OK","LOADED","READY","ACTIVE"]

def splash():
    os.system("clear" if os.name == "posix" else "cls")
    print(B); time.sleep(0.3)
    for _ in range(6):
        print(f"\033[1;32m[+]\033[0m [{random.choice(TAGS)}] \033[1;33m{random.choice(MODS)}\033[0m \033[1;32m{random.choice(STAT)}\033[0m")
        time.sleep(0.06)
    for c in "█▓▒░█▓▒░█▓▒░": print(f"\033[1;31m{c}\033[0m", end="", flush=True); time.sleep(0.015)
    print("\n")

def auth():
    print("\033[1;36m╔══════════════════════════════════════╗\033[0m")
    print("\033[1;36m║       TELEGRAM AUTH REQUIRED         ║\033[0m")
    print("\033[1;36m╚══════════════════════════════════════╝\033[0m\n")
    a = input("\033[1;32m[→] API ID:\033[0m ").strip()
    b = input("\033[1;32m[→] API HASH:\033[0m ").strip()
    c = input("\033[1;32m[→] BOT TOKEN:\033[0m ").strip()
    print("\033[1;33m[+] CONNECTING...\033[0m"); time.sleep(0.5)
    print("\033[1;32m[+] AUTHENTICATED\n\033[0m")
    return int(a), b, c

class Hunter:
    def __init__(self):
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"})
    
    def search_ddg(self, q, n=5):
        r = []
        try:
            x = self.s.get(f"https://html.duckduckgo.com/html/?q={quote_plus(q)}", timeout=10)
            if x.status_code == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(x.text, "html.parser")
                for res in soup.select(".result"):
                    a = res.select_one(".result__a")
                    if a:
                        lk = a.get("href","")
                        if "uddg=" in lk:
                            from urllib.parse import unquote
                            lk = unquote(lk.split("uddg=")[1].split("&")[0])
                        sn = res.select_one(".result__snippet")
                        sn = sn.text[:200] if sn else ""
                        if lk and a.text: r.append({"t":a.text,"u":lk,"s":sn})
        except: pass
        return r
    
    def hunt(self, queries, n=6):
        all_r = []; seen = set()
        for q in queries:
            if len(all_r) >= n: break
            time.sleep(0.3 + random.random() * 0.2)
            for r in self.search_ddg(q, 5):
                try: d = r["u"].split("/")[2]
                except: continue
                if d not in seen:
                    seen.add(d)
                    all_r.append(r)
                if len(all_r) >= n: break
        return all_r[:n]

def main():
    splash()
    aid, ah, tok = auth()
    
    from bs4 import BeautifulSoup
    bot = TelegramClient("ds", aid, ah).start(bot_token=tok)
    us = {}
    
    @bot.on(events.NewMessage(pattern="/start"))
    async def s(e):
        await e.reply(f"`{B}`\n**⚔️ DEDSEC HUNTER**\n\n/hunt - Search\n/cats - Categories\n/quick <cat> <n>", parse_mode="md")
    
    @bot.on(events.NewMessage(pattern="/cats"))
    async def c(e):
        await e.reply("**CATEGORIES:**\n" + "\n".join(CATS.keys()), parse_mode="md")
    
    @bot.on(events.NewMessage(pattern="/hunt"))
    async def h(e):
        uid = e.sender_id; us[uid] = {"s":"cat"}
        btns=[]; row=[]
        for i,cat in enumerate(CATS.keys()):
            row.append(Button.inline(cat[:20],f"c_{i}"))
            if len(row)==2: btns.append(row); row=[]
        if row: btns.append(row)
        await e.reply("**🎯 SELECT CATEGORY**", buttons=btns, parse_mode="md")
    
    @bot.on(events.CallbackQuery)
    async def cb(e):
        uid=e.sender_id; d=e.data.decode()
        if d.startswith("c_"):
            i=int(d.split("_")[1]); cat=list(CATS.keys())[i]
            us[uid]={"s":"cnt","cat":cat}
            await e.edit(f"**{cat}**\n\nResults? (1-15):")
    
    @bot.on(events.NewMessage)
    async def m(e):
        if e.text.startswith("/"): return
        uid=e.sender_id; s=us.get(uid)
        if not s or s.get("s")!="cnt": return
        try: n=int(e.text.strip());
        except: await e.reply("⚠️ Number 1-15"); return
        if n<1 or n>15: await e.reply("⚠️ 1-15"); return
        
        cat=s["cat"]; qs=CATS[cat]
        msg=await e.reply(f"**🔍 HUNTING {cat}...**")
        
        hh=Hunter(); r=hh.hunt(qs, n)
        
        if not r:
            await msg.edit(f"**❌ NOTHING FOUND** for {cat}\n_Try another category_")
            return
        
        lines=[f"**╔══ DEDSEC REPORT ══╗**\n**{cat}** | {len(r)}/{n}\n"+"═"*35]
        for i,x in enumerate(r):
            tag=cat.split(" ")[0].replace("🌑","").replace("📦","").replace("🎮","").replace("🔓","").replace("🤖","").replace("🐍","").replace("🌐","").replace("🛠️","").replace("💀","").strip() or cat[:3]
            lines.append(f"**{i+1}.** {x['t'][:80]}\n`[{tag}]`\n{x['s'][:200]}\n{x['u']}\n"+"─"*35)
        lines.append("\n/hunt again")
        
        txt="\n".join(lines)
        if len(txt)>4000:
            await msg.edit(lines[0])
            for ch in [lines[i:i+3] for i in range(1,len(lines),3)]:
                await e.reply("\n".join(ch))
        else: await msg.edit(txt)
        del us[uid]
    
    @bot.on(events.NewMessage(pattern="/quick (.+)"))
    async def q(e):
        try:
            a=e.pattern_match.group(1).strip()
            p=a.rsplit(" ",1); cn=p[0].lower()
            n=max(1,min(15,int(p[1]))) if len(p)>1 else 5
        except:
            await e.reply("/quick <cat> <n>\nEx: /quick gamehacks 5"); return
        mc=None
        for c in CATS:
            if cn in c.lower().replace("&","").replace(" ",""): mc=c; break
        if not mc: await e.reply("Not found. /cats"); return
        
        hh=Hunter(); msg=await e.reply(f"**⚡ {mc}**")
        r=hh.hunt(CATS[mc], n)
        if not r: await msg.edit(f"**❌ Nothing**"); return
        lines=[f"**⚡ QUICK HUNT**\n**{mc}** | {len(r)}/{n}\n"+"═"*35]
        for i,x in enumerate(r):
            tag=mc.split(" ")[0].replace("🌑","").replace("📦","").replace("🎮","").strip() or mc[:3]
            lines.append(f"**{i+1}.** {x['t'][:80]}\n`[{tag}]`\n{x['s'][:200]}\n{x['u']}\n"+"─"*35)
        await msg.edit("\n".join(lines))
    
    print("\033[1;32m[+] DEDSEC HUNTER RUNNING\033[0m")
    bot.run_until_disconnected()

if __name__ == "__main__":
    main()
