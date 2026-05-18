#!/usr/bin/env python3
import os, re, time, json, random, requests
from urllib.parse import quote_plus, unquote
from bs4 import BeautifulSoup
from telethon import TelegramClient, events, Button

BANNER = """
╔══════════════════════════════════════════╗
║        ██████╗ ███████╗██████╗ ███████╗ ░
║        ██╔══██╗██╔════╝██╔══██╗██╔════╝ ░
║        ██║  ██║█████╗  ██║  ██║███████╗ ░
║        ██║  ██║██╔══╝  ██║  ██║╚════██║ ░
║        ██████╔╝███████╗██████╔╝███████║ ░
║        ╚═════╝ ╚══════╝╚═════╝ ╚══════╝ ░
║     ░░░▒▒▒▓▓▓ HUNTER v1.0 ▓▓▓▒▒▒░░░     ║
║   [ Telegram Aggregator | Pentest Only ]  ║
╚══════════════════════════════════════════╝
"""

CATEGORIES = {
    "🎮 Game Hacks": ["pubg hack cheat aimbot", "fortnite hack undetected", "valorant cheat", "apex hack", "warzone cheat", "game hacking bypass"],
    "🔓 Account Dumps": ["account dump combo list", "credential leak pastebin", "account checker tool", "email password dump"],
    "🤖 AI Hacking": ["ai jailbreak prompt", "llm exploitation tool", "chatgpt prompt leak", "ai red team"],
    "🐍 Python Tools": ["python hacking tool", "python exploit poc", "python reverse shell", "python scraper osint"],
    "🌐 Social Media": ["instagram hack tool", "telegram scraper bot", "discord token grabber", "facebook brute"],
    "🛠️ Hacking Tools": ["pentest tool kali", "sqlmap automation", "xss scanner bypass", "reverse shell generator"],
    "💀 RAT & Malware": ["rat telegram remote", "python stealer", "info stealer source", "fud crypter"],
    "🌑 Deep Forums": ["site:altenens.is hack", "site:altenens.is dump", "site:altenens.is cheat", "site:altenens.is tool"],
    "📦 GitHub": ["site:github.com pubg cheat", "site:github.com account checker", "site:github.com reverse shell", "site:github.com instagram brute"],
}

class Hunter:
    def __init__(self):
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"})
    
    def search(self, query, n=5):
        results = []
        try:
            r = self.s.get(f"https://www.google.com/search?q={quote_plus(query)}&num={n}", timeout=10)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "html.parser")
                for g in soup.select("div.g"):
                    a = g.find("a")
                    h3 = g.find("h3")
                    if a and h3:
                        link = a.get("href","")
                        if link.startswith("/url?q="): link = unquote(link.split("/url?q=")[1].split("&")[0])
                        snip = g.find("div", class_="VwiC3b")
                        snip = snip.text[:200] if snip else ""
                        if link and h3.text: results.append({"t": h3.text, "u": link, "s": snip})
            # fallback ddg
            r2 = self.s.get(f"https://html.duckduckgo.com/html/?q={quote_plus(query)}", timeout=10)
            if r2.status_code == 200:
                soup = BeautifulSoup(r2.text, "html.parser")
                for res in soup.select(".result"):
                    a = res.select_one(".result__a")
                    if a:
                        link = a.get("href","")
                        if "uddg=" in link: link = unquote(link.split("uddg=")[1].split("&")[0])
                        snip = res.select_one(".result__snippet")
                        snip = snip.text[:200] if snip else ""
                        if link and a.text: results.append({"t": a.text, "u": link, "s": snip})
        except: pass
        seen = set()
        final = []
        for r in results:
            d = r["u"].split("/")[2] if "://" in r["u"] else r["u"]
            if d not in seen: seen.add(d); final.append(r)
        return final[:n]

def ask_creds():
    print("[!] DEDSEC HUNTER needs Telegram credentials to start.")
    api_id = input("[?] Enter your API ID (from my.telegram.org): ").strip()
    api_hash = input("[?] Enter your API HASH (from my.telegram.org): ").strip()
    bot_token = input("[?] Enter your BOT TOKEN (from @BotFather): ").strip()
    return int(api_id), api_hash, bot_token

# ─── AUTH ON START ──────────────────────────────────────────────────────
API_ID, API_HASH, BOT_TOKEN = ask_creds()
print("\n[+] Credentials set. Starting bot...\n")

bot = TelegramClient("dedsec_session", API_ID, API_HASH).start(bot_token=BOT_TOKEN)
user_sessions = {}

def fmt(idx, t, u, s, cat):
    return f"**{idx}.** {t[:80]}\n`[{cat}]`\n{s[:150]}\n{u}\n" + "─"*35

@bot.on(events.NewMessage(pattern="/start"))
async def start(e):
    await e.reply(f"`{BANNER}`\n**⚔️ DEDSEC HUNTER ONLINE ⚔️**\n\n/hunt - Start hunt\n/cats - Categories\n/help - Help", parse_mode="md")

@bot.on(events.NewMessage(pattern="/help"))
async def help(e):
    txt = "**DEDSEC HUNTER**\n/hunt - Choose category + how many results\n/cats - List categories\n/quick <cat> <n> - Fast search\n\n**Categories:**\n" + "\n".join(CATEGORIES.keys())
    await e.reply(txt, parse_mode="md")

@bot.on(events.NewMessage(pattern="/cats"))
async def cats(e):
    await e.reply("**Categories:**\n" + "\n".join(CATEGORIES.keys()), parse_mode="md")

@bot.on(events.NewMessage(pattern="/hunt"))
async def hunt(e):
    uid = e.sender_id
    user_sessions[uid] = {"step": "cat"}
    btns = []
    row = []
    for i, cat in enumerate(CATEGORIES.keys()):
        row.append(Button.inline(cat, f"c_{i}"))
        if len(row) == 2: btns.append(row); row = []
    if row: btns.append(row)
    await e.reply("**🎯 SELECT CATEGORY**", buttons=btns, parse_mode="md")

@bot.on(events.CallbackQuery)
async def cb(e):
    uid = e.sender_id
    data = e.data.decode()
    if data.startswith("c_"):
        idx = int(data.split("_")[1])
        cat = list(CATEGORIES.keys())[idx]
        user_sessions[uid] = {"step": "count", "cat": cat}
        await e.edit(f"**✅ {cat}**\n\nHow many results? (1-15):")

@bot.on(events.NewMessage)
async def msg(e):
    if e.text.startswith("/"): return
    uid = e.sender_id
    s = user_sessions.get(uid)
    if not s or s.get("step") != "count": return
    try:
        n = int(e.text.strip())
        if n < 1 or n > 15: raise ValueError
    except:
        await e.reply("⚠️ Number 1-15 only.")
        return
    
    cat = s["cat"]
    queries = CATEGORIES[cat]
    h = Hunter()
    
    m = await e.reply(f"**🔍 Hunting {cat}...**")
    
    all_r = []
    seen = set()
    for q in queries:
        if len(all_r) >= n: break
        time.sleep(0.3 + random.random() * 0.3)
        res = h.search(q, 3)
        for r in res:
            d = r["u"].split("/")[2] if "://" in r["u"] else r["u"]
            if d not in seen: seen.add(d); all_r.append(r)
        if len(all_r) >= n: break
    all_r = all_r[:n]
    
    if not all_r:
        await m.edit(f"**❌ Nothing for {cat}**")
        return
    
    lines = [f"**╔══ DEDSEC HUNTER RESULTS ══╗**\n**Category:** {cat}\n**Results:** {len(all_r)}/{n}\n" + "═"*35]
    for i, r in enumerate(all_r):
        lines.append(fmt(i+1, r["t"], r["u"], r["s"], cat))
    lines.append(f"\n_/hunt again_")
    
    txt = "\n".join(lines)
    if len(txt) > 4000:
        await m.edit(lines[0])
        for chunk in [lines[i:i+3] for i in range(1, len(lines), 3)]:
            await e.reply("\n".join(chunk))
    else:
        await m.edit(txt)
    
    del user_sessions[uid]

@bot.on(events.NewMessage(pattern="/quick (.+)"))
async def quick(e):
    try:
        args = e.pattern_match.group(1).strip()
        parts = args.rsplit(" ", 1)
        cn = parts[0].lower()
        n = max(1, min(15, int(parts[1]))) if len(parts) > 1 else 5
    except:
        await e.reply("Usage: /quick <cat> <n>\nEx: /quick gamehacks 5")
        return
    mc = None
    for c in CATEGORIES:
        if cn in c.lower().replace("&","").replace(" ",""): mc = c; break
    if not mc: await e.reply("Category not found. /cats"); return
    
    h = Hunter()
    m = await e.reply(f"**⚡ {mc}...**")
    all_r = []; seen = set()
    for q in CATEGORIES[mc]:
        if len(all_r) >= n: break
        time.sleep(0.3)
        for r in h.search(q, 3):
            d = r["u"].split("/")[2] if "://" in r["u"] else r["u"]
            if d not in seen: seen.add(d); all_r.append(r)
    all_r = all_r[:n]
    if not all_r: await m.edit(f"**❌ Nothing**"); return
    lines = [f"**⚡ QUICK HUNT ⚡**\n**{mc}** | {len(all_r)}/{n}\n" + "═"*35]
    for i, r in enumerate(all_r): lines.append(fmt(i+1, r["t"], r["u"], r["s"], mc))
    await m.edit("\n".join(lines))

print("[+] DEDSEC HUNTER RUNNING")
bot.run_until_disconnected()
