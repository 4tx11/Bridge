#!/usr/bin/env python3
"""
DEDSEC HUNTER v1.0 - Telegram Intelligence Aggregator
"""
import sys, time, os, random, requests, json
from urllib.parse import quote_plus, unquote
from bs4 import BeautifulSoup

# ─── FAST SPLASH ──────────────────────────────────────────────────────────
S = """
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
    "🎮 Game Hacks": ["pubg hack cheat aimbot", "fortnite hack undetected", "valorant cheat", "game hacking bypass"],
    "🔓 Account Dumps": ["account dump combo list", "credential leak pastebin", "account checker"],
    "🤖 AI Hacking": ["ai jailbreak prompt", "llm exploitation", "chatgpt prompt leak"],
    "🐍 Python Tools": ["python hacking tool", "python exploit poc", "python reverse shell"],
    "🌐 Social Media": ["instagram hack tool", "telegram scraper", "discord token grabber"],
    "🛠️ Hacking Tools": ["pentest tool kali", "sqlmap automation", "reverse shell generator"],
    "💀 Malware": ["rat telegram remote", "python stealer", "info stealer source"],
    "🌑 Deep Forums": ["site:altenens.is hack", "site:altenens.is dump", "site:altenens.is cheat"],
    "📦 GitHub": ["site:github.com pubg cheat", "site:github.com account checker", "site:github.com reverse shell"],
}

PH = ["\033[1;32m[+]","\033[1;33m[*]","\033[1;34m[>]","\033[1;35m[~]"]
SP = ["\033[1;32mOK\033[0m","\033[1;33mLOADED\033[0m","\033[1;34mREADY\033[0m","\033[1;35mACTIVE\033[0m"]
MOD = ["KERNEL","CORE","ENGINE","CACHE","STREAM","PROXY","SOCKET","THREAD","BUFFER","SCAN"]
TAGS = ["INIT","LOAD","AUTH","SYNC","SCAN","PARSE","DECODE","FETCH","CACHE","HOOK","MAP"]

def ff():
    for c in "█▓▒░█▓▒░█▓▒░": print(f"\033[1;31m{c}\033[0m", end="", flush=True); time.sleep(0.02)
    print()

def splash():
    os.system("clear" if os.name == "posix" else "cls")
    print(S)
    time.sleep(0.3)
    for _ in range(6):
        m = random.choice(MOD)
        p = random.choice(PH)
        t = random.choice(TAGS)
        s = random.choice(SP)
        print(f"{p} [{t}] {m}.sys {s}")
        time.sleep(0.06 + random.random() * 0.05)
    ff()
    print(f"\033[1;36m{'═'*50}\033[0m")
    time.sleep(0.2)

def get_creds():
    print(f"\033[1;33m[?] TELEGRAM CREDENTIALS\033[0m")
    print(f"\033[1;30m{'-'*40}\033[0m")
    a = input(f"\033[1;32m[→]\033[0m API ID: \033[1;37m")
    print("\033[0m",end="")
    b = input(f"\033[1;32m[→]\033[0m API HASH: \033[1;37m")
    print("\033[0m",end="")  
    c = input(f"\033[1;32m[→]\033[0m BOT TOKEN: \033[1;37m")
    print("\033[0m",end="")
    print(f"\n\033[1;33m[+] AUTHENTICATING...\033[0m")
    time.sleep(0.5)
    print(f"\033[1;32m[+] SESSION ESTABLISHED\033[0m\n")
    return int(a), b, c

class H:
    def __init__(self):
        self.s = requests.Session()
        self.s.headers.update({"UA": "Mozilla/5.0"})
    def search(self, q, n=5):
        r = []
        try:
            x = self.s.get(f"https://www.google.com/search?q={quote_plus(q)}&num={n}", timeout=8)
            if x.status_code == 200:
                soup = BeautifulSoup(x.text, "html.parser")
                for g in soup.select("div.g"):
                    a = g.find("a"); h3 = g.find("h3")
                    if a and h3:
                        lk = a.get("href","")
                        if lk.startswith("/url?q="): lk = unquote(lk.split("/url?q=")[1].split("&")[0])
                        sn = g.find("div",class_="VwiC3b")
                        sn = sn.text[:150] if sn else ""
                        if lk and h3.text: r.append({"t":h3.text,"u":lk,"s":sn})
        except: pass
        # ddg fallback
        try:
            x = self.s.get(f"https://html.duckduckgo.com/html/?q={quote_plus(q)}", timeout=8)
            if x.status_code == 200:
                soup = BeautifulSoup(x.text, "html.parser")
                for res in soup.select(".result"):
                    a = res.select_one(".result__a")
                    if a:
                        lk = a.get("href","")
                        if "uddg=" in lk: lk = unquote(lk.split("uddg=")[1].split("&")[0])
                        sn = res.select_one(".result__snippet")
                        sn = sn.text[:150] if sn else ""
                        if lk and a.text: r.append({"t":a.text,"u":lk,"s":sn})
        except: pass
        seen = set()
        f = []
        for x in r:
            d = x["u"].split("/")[2] if "://" in x["u"] else x["u"]
            if d not in seen: seen.add(d); f.append(x)
        return f[:n]

def main():
    splash()
    aid, ahash, token = get_creds()
    
    from telethon import TelegramClient, events, Button
    bot = TelegramClient("ds", aid, ahash).start(bot_token=token)
    us = {}
    
    @bot.on(events.NewMessage(pattern="/start"))
    async def s(e):
        await e.reply(f"`{S}`\n**⚔️ DEDSEC HUNTER**\n\n/hunt\n/cats\n/quick `<cat>` `<n>`", parse_mode="md")
    
    @bot.on(events.NewMessage(pattern="/cats"))
    async def c(e):
        await e.reply("**CATEGORIES:**\n"+"\n".join(CATS.keys()), parse_mode="md")
    
    @bot.on(events.NewMessage(pattern="/hunt"))
    async def h(e):
        uid = e.sender_id
        us[uid] = {"s":"cat"}
        btns=[]; row=[]
        for i,cat in enumerate(CATS.keys()):
            row.append(Button.inline(cat[:20],f"c_{i}"))
            if len(row)==2: btns.append(row); row=[]
        if row: btns.append(row)
        await e.reply("**🎯 SELECT CATEGORY**", buttons=btns, parse_mode="md")
    
    @bot.on(events.CallbackQuery)
    async def cb(e):
        uid=e.sender_id
        d=e.data.decode()
        if d.startswith("c_"):
            i=int(d.split("_")[1])
            cat=list(CATS.keys())[i]
            us[uid]={"s":"cnt","cat":cat}
            await e.edit(f"**{cat}**\n\nResults? (1-15):")
    
    @bot.on(events.NewMessage)
    async def m(e):
        if e.text.startswith("/"): return
        uid=e.sender_id
        s=us.get(uid)
        if not s or s.get("s")!="cnt": return
        try:
            n=int(e.text.strip())
            if n<1 or n>15: raise
        except:
            await e.reply("⚠️ 1-15 only"); return
        
        cat=s["cat"]
        qs=CATS[cat]
        msg=await e.reply(f"**🔍 Hunting {cat}...**")
        
        hh=H()
        all_r=[]; seen=set()
        for q in qs:
            if len(all_r)>=n: break
            time.sleep(0.2+random.random()*0.2)
            for r in hh.search(q,3):
                d=r["u"].split("/")[2] if "://" in r["u"] else r["u"]
                if d not in seen: seen.add(d); all_r.append(r)
                if len(all_r)>=n: break
        all_r=all_r[:n]
        
        if not all_r:
            await msg.edit(f"**❌ No results for {cat}**"); return
        
        lines=[f"**╔══ DEDSEC REPORT ══╗**\n**{cat}** | {len(all_r)}/{n}\n"+"═"*35]
        for i,r in enumerate(all_r):
            tag=cat.split(" ")[0]
            lines.append(f"**{i+1}.** {r['t'][:80]}\n`[{tag}]`\n{r['s'][:150]}\n{r['u']}\n"+"─"*35)
        lines.append("\n/hunt again")
        
        txt="\n".join(lines)
        if len(txt)>4000:
            await msg.edit(lines[0])
            for chunk in [lines[i:i+3] for i in range(1,len(lines),3)]:
                await e.reply("\n".join(chunk))
        else:
            await msg.edit(txt)
        del us[uid]
    
    @bot.on(events.NewMessage(pattern="/quick (.+)"))
    async def q(e):
        try:
            a=e.pattern_match.group(1).strip()
            p=a.rsplit(" ",1)
            cn=p[0].lower()
            n=max(1,min(15,int(p[1]))) if len(p)>1 else 5
        except:
            await e.reply("/quick <cat> <n>\n/gamehacks 5"); return
        mc=None
        for c in CATS:
            if cn in c.lower().replace("&","").replace(" ",""): mc=c; break
        if not mc: await e.reply("Not found. /cats"); return
        
        hh=H()
        msg=await e.reply(f"**⚡ {mc}**")
        all_r=[]; seen=set()
        for q in CATS[mc]:
            if len(all_r)>=n: break
            time.sleep(0.2)
            for r in hh.search(q,3):
                d=r["u"].split("/")[2] if "://" in r["u"] else r["u"]
                if d not in seen: seen.add(d); all_r.append(r)
                if len(all_r)>=n: break
        all_r=all_r[:n]
        if not all_r: await msg.edit(f"**❌ Nothing**"); return
        lines=[f"**⚡ QUICK HUNT**\n**{mc}** | {len(all_r)}/{n}\n"+"═"*35]
        for i,r in enumerate(all_r):
            tag=mc.split(" ")[0]
            lines.append(f"**{i+1}.** {r['t'][:80]}\n`[{tag}]`\n{r['s'][:150]}\n{r['u']}\n"+"─"*35)
        await msg.edit("\n".join(lines))
    
    print(f"\033[1;32m[+] DEDSEC HUNTER RUNNING\033[0m")
    print(f"\033[1;30m[Ctrl+C to stop]\033[0m")
    bot.run_until_disconnected()

if __name__ == "__main__":
    main()
