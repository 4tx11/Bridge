#!/usr/bin/env python3
import sys, time, os, random, requests, json
from urllib.parse import quote_plus, unquote
from bs4 import BeautifulSoup
from telethon import TelegramClient, events, Button

B = """
\033[1;31m╔══════════════════════════════════════════╗
║        ██████╗ ███████╗██████╗ ███████╗ ║
║        ██╔══██╗██╔════╝██╔══██╗██╔════╝ ║
║        ██║  ██║█████╗  ██║  ██║███████╗ ║
║        ██║  ██║██╔══╝  ██║  ██║╚════██║ ║
║        ██████╔╝███████╗██████╔╝███████║ ║
║        ╚═════╝ ╚══════╝╚═════╝ ╚══════╝ ║
║     ░░░▒▒▒▓▓▓ HUNTER v2.0 ▓▓▓▒▒▒░░░     ║
╚══════════════════════════════════════════╝\033[0m
"""

CATS = {
    "🎮 Game Hacks": ["pubg hack cheat", "fortnite aimbot esp", "valorant wallhack", "game hacking tool"],
    "🔓 Account Dumps": ["email password combo list", "account dump database", "credential leak pastebin"],
    "🤖 AI Hacking": ["ai jailbreak prompt", "chatgpt leak system prompt", "llm red team exploit"],
    "🐍 Python Tools": ["python reverse shell", "python keylogger source", "python exploit poc"],
    "🌐 Social Media": ["instagram hack python", "telegram osint scraper", "discord token grabber"],
    "🛠️ Hacking Tools": ["sql injection tool", "xss payload generator", "reverse shell payload"],
    "💀 Malware": ["rat remote access python", "info stealer source", "keylogger undetected"],
    "🌑 Altenen": ["altenen.is hack", "altenen.is account dump", "altenen.is cheat"],
    "📦 GitHub": ["github.com pubg cheat", "github.com account checker", "github.com reverse shell"],
}

def anis():
    os.system("clear" if os.name == "posix" else "cls")
    print(B); time.sleep(0.2)
    for _ in range(5):
        print(f"\033[1;32m[+]\033[0m [{random.choice(['INIT','LOAD','AUTH','SYNC','SCAN'])}] {random.choice(['kernel','core','agent','stream','proxy'])}.sys \033[1;32m{random.choice(['OK','LOADED','READY'])}\033[0m")
        time.sleep(0.06)
    for c in "█▓▒░█▓▒░█▓▒░": print(f"\033[1;31m{c}\033[0m", end="", flush=True); time.sleep(0.01)
    print("\n")

def creds():
    print("\033[1;36m╔══════════════════════════════════════╗\033[0m")
    print("\033[1;36m║       TELEGRAM CREDENTIALS           ║\033[0m")
    print("\033[1;36m╚══════════════════════════════════════╝\033[0m\n")
    a = input("\033[1;32m[→] API ID:\033[0m ").strip()
    b = input("\033[1;32m[→] API HASH:\033[0m ").strip()
    c = input("\033[1;32m[→] BOT TOKEN:\033[0m ").strip()
    print("\033[1;33m[+] AUTH...\033[0m"); time.sleep(0.4)
    print("\033[1;32m[+] READY\n\033[0m")
    return int(a), b, c

class Eng:
    def __init__(self):
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"})
    
    def bing(self, q, n=5):
        r = []
        try:
            x = self.s.get(f"https://www.bing.com/search?q={quote_plus(q)}&count={n}", timeout=10)
            if x.status_code == 200:
                soup = BeautifulSoup(x.text, "html.parser")
                for li in soup.select("#b_results li.b_algo"):
                    a = li.select_one("h2 a")
                    if a:
                        lk = a.get("href","")
                        sn = li.select_one(".b_caption p")
                        sn = sn.text[:200] if sn else ""
                        if lk and a.text: r.append({"t":a.text,"u":lk,"s":sn})
        except: pass
        return r
    
    def hunt(self, qs, n=6):
        a=[]; seen=set()
        for q in qs:
            if len(a)>=n: break
            time.sleep(0.3+random.random()*0.2)
            for r in self.bing(q,5):
                try: d=r["u"].split("/")[2]
                except: continue
                if d not in seen: seen.add(d); a.append(r)
                if len(a)>=n: break
        return a[:n]

def main():
    anis()
    aid, ah, tok = creds()
    
    bot = TelegramClient("ds", aid, ah).start(bot_token=tok)
    us = {}
    
    @bot.on(events.NewMessage(pattern="/start"))
    async def s(e):
        await e.reply(f"`{B}`\n**⚔️ DEDSEC HUNTER v2**\n\n/hunt - Search\n/cats - Categories\n/quick <cat> <n>", parse_mode="md")
    
    @bot.on(events.NewMessage(pattern="/cats"))
    async def c(e):
        await e.reply("**CATEGORIES:**\n"+ "\n".join(CATS.keys()), parse_mode="md")
    
    @bot.on(events.NewMessage(pattern="/hunt"))
    async def h(e):
        uid=e.sender_id; us[uid]={"s":"cat"}
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
        try: n=int(e.text.strip())
        except: await e.reply("⚠️ 1-15"); return
        if n<1 or n>15: await e.reply("⚠️ 1-15"); return
        
        cat=s["cat"]; qs=CATS[cat]
        msg=await e.reply(f"**🔍 {cat}...**")
        eng=Eng(); r=eng.hunt(qs,n)
        
        if not r:
            await msg.edit(f"**❌ No results** for {cat}\n_Try again_")
            return
        
        lines=[f"**╔══ DEDSEC REPORT ══╗**\n**{cat}** | {len(r)}/{n}\n"+"═"*35]
        for i,x in enumerate(r):
            ln = x["u"].split("//")[-1].split("/")[0] if "//" in x["u"] else x["u"]
            lines.append(f"**{i+1}.** {x['t'][:80]}\n`[{cat[:2]}]` {ln}\n{x['s'][:200]}\n{x['u']}\n"+"─"*35)
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
        
        eng=Eng(); msg=await e.reply(f"**⚡ {mc}**")
        r=eng.hunt(CATS[mc],n)
        if not r: await msg.edit("**❌ Nothing**"); return
        lines=[f"**⚡ QUICK HUNT**\n**{mc}** | {len(r)}/{n}\n"+"═"*35]
        for i,x in enumerate(r):
            ln = x["u"].split("//")[-1].split("/")[0] if "//" in x["u"] else x["u"]
            lines.append(f"**{i+1}.** {x['t'][:80]}\n`[{mc[:2]}]` {ln}\n{x['s'][:200]}\n{x['u']}\n"+"─"*35)
        await msg.edit("\n".join(lines))
    
    print("\033[1;32m[+] DEDSEC ACTIVE\033[0m")
    bot.run_until_disconnected()

if __name__ == "__main__":
    main()
