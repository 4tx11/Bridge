#!/usr/bin/env python3
# DEDSEC PROXY FARM BOT - Telegram controlled proxy harvester
# Commands: /harvest, /proxies, /export_proxies, /proxy_status

import asyncio
import os
import re
import time
import json
import random
import threading
import requests
import sqlite3
from datetime import datetime
from queue import Queue
from bs4 import BeautifulSoup
from telethon import TelegramClient, events
from telethon.tl.types import Message

# ========== CONFIGURATION ==========
PROXY_DB = "proxy_farm.db"
TARGET_URLS = [
    "https://accounts.google.com/signup",
    "https://www.instagram.com/",
    "https://www.tiktok.com/",
    "https://accounts.snapchat.com/"
]
VALID_TIMEOUT = 10
MAX_PROXIES = 500
REFILL_INTERVAL = 1800  # seconds (30 min)

# Free proxy sources
SOURCES = [
    ("https://free-proxy-list.net/", "table"),
    ("https://www.sslproxies.org/", "table"),
    ("https://www.us-proxy.org/", "table"),
    ("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all", "text"),
    ("https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt", "text"),
    ("https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt", "text"),
    ("https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt", "text"),
]

# ========== DATABASE FUNCTIONS ==========
def init_db():
    conn = sqlite3.connect(PROXY_DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS proxies
                 (id INTEGER PRIMARY KEY,
                  proxy TEXT UNIQUE,
                  protocol TEXT,
                  last_checked TEXT,
                  success_count INTEGER,
                  fail_count INTEGER,
                  latency REAL)''')
    conn.commit()
    conn.close()

def save_proxy(proxy, protocol, latency):
    conn = sqlite3.connect(PROXY_DB)
    c = conn.cursor()
    try:
        c.execute('''INSERT INTO proxies (proxy, protocol, last_checked, success_count, fail_count, latency)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (proxy, protocol, datetime.now().isoformat(), 1, 0, latency))
    except sqlite3.IntegrityError:
        c.execute('''UPDATE proxies SET last_checked=?, success_count=success_count+1, latency=?
                     WHERE proxy=?''',
                  (datetime.now().isoformat(), latency, proxy))
    conn.commit()
    conn.close()

def mark_failed(proxy):
    conn = sqlite3.connect(PROXY_DB)
    c = conn.cursor()
    c.execute('''UPDATE proxies SET fail_count=fail_count+1 WHERE proxy=?''', (proxy,))
    conn.commit()
    conn.close()

def get_working_proxies(limit=100, min_success=1):
    conn = sqlite3.connect(PROXY_DB)
    c = conn.cursor()
    c.execute('''SELECT proxy, protocol FROM proxies 
                 WHERE success_count > ? AND fail_count < 5
                 ORDER BY latency ASC LIMIT ?''', (min_success, limit))
    rows = c.fetchall()
    conn.close()
    return [{"proxy": row[0], "protocol": row[1]} for row in rows]

def get_proxy_count():
    conn = sqlite3.connect(PROXY_DB)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM proxies WHERE fail_count < 5")
    count = c.fetchone()[0]
    conn.close()
    return count

# ========== PROXY SCRAPER ==========
def scrape_free_proxies():
    new_proxies = []
    for url, style in SOURCES:
        try:
            resp = requests.get(url, timeout=15)
            if style == "table":
                soup = BeautifulSoup(resp.text, 'html.parser')
                table = soup.find('table')
                if table:
                    rows = table.find_all('tr')
                    for row in rows[1:]:
                        cells = row.find_all('td')
                        if len(cells) >= 2:
                            ip = cells[0].text.strip()
                            port = cells[1].text.strip()
                            proxy = f"{ip}:{port}"
                            new_proxies.append(("http", proxy))
            elif style == "text":
                for line in resp.text.splitlines():
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '://' in line:
                            parts = line.split('://')
                            protocol = parts[0]
                            proxy = parts[1]
                        else:
                            protocol = 'http'
                            proxy = line
                        new_proxies.append((protocol, proxy))
            time.sleep(0.5)
        except Exception:
            pass
    return new_proxies

# ========== PROXY VALIDATOR ==========
def test_proxy(proxy_info):
    protocol = proxy_info[0]
    proxy_str = proxy_info[1]
    proxy_url = f"{protocol}://{proxy_str}"
    proxies_dict = {"http": proxy_url, "https": proxy_url}
    target = random.choice(TARGET_URLS)
    start = time.time()
    try:
        resp = requests.get(target, proxies=proxies_dict, timeout=VALID_TIMEOUT, 
                            headers={"User-Agent": "Mozilla/5.0"})
        latency = time.time() - start
        if resp.status_code in [200, 302, 301, 403, 429]:
            save_proxy(proxy_str, protocol, latency)
            return True
        else:
            mark_failed(proxy_str)
            return False
    except:
        mark_failed(proxy_str)
        return False

def validator_worker(queue, results):
    while True:
        item = queue.get()
        if item is None:
            break
        ok = test_proxy(item)
        if ok:
            results.append(item)
        queue.task_done()

def harvest_and_validate():
    init_db()
    raw = scrape_free_proxies()
    if not raw:
        return 0
    q = Queue()
    results = []
    threads = []
    for _ in range(20):
        t = threading.Thread(target=validator_worker, args=(q, results))
        t.start()
        threads.append(t)
    for p in raw:
        q.put(p)
    q.join()
    for _ in range(20):
        q.put(None)
    for t in threads:
        t.join()
    # Clean old failed proxies
    conn = sqlite3.connect(PROXY_DB)
    c = conn.cursor()
    c.execute("DELETE FROM proxies WHERE fail_count >= 5")
    conn.commit()
    conn.close()
    return len(results)

# ========== TELEGRAM BOT ==========
class ProxyFarmBot:
    def __init__(self, api_id, api_hash, bot_token):
        self.client = TelegramClient('proxy_farm_bot', api_id, api_hash)
        self.bot_token = bot_token
        self.harvesting = False

    async def start(self):
        await self.client.start(bot_token=self.bot_token)
        print("[DEDSEC] Proxy Farm Bot online.")

        @self.client.on(events.NewMessage(pattern='/start'))
        async def start_cmd(event):
            await event.reply("""💀 **DEDSEC PROXY FARM BOT** 💀

Commands:
/harvest – Scrape & validate fresh proxies (takes 1-2 min)
/proxies – List first 20 working proxies
/export_proxies – Send all working proxies as file
/proxy_status – Show number of working proxies
/stop_harvest – Cancel running harvest (if any)""")

        @self.client.on(events.NewMessage(pattern='/harvest'))
        async def harvest_cmd(event):
            if self.harvesting:
                await event.reply("❌ Harvest already in progress. Wait or /stop_harvest")
                return
            self.harvesting = True
            await event.reply("🔍 **Harvesting proxies...** This may take 1-2 minutes.\nScraping 7+ sources and validating against target platforms.")
            # Run in thread to not block bot
            loop = asyncio.get_event_loop()
            count = await loop.run_in_executor(None, harvest_and_validate)
            self.harvesting = False
            await event.reply(f"✅ Harvest complete. **{count}** new valid proxies added.\nTotal working: {get_proxy_count()}\nUse `/proxies` to view.")

        @self.client.on(events.NewMessage(pattern='/stop_harvest'))
        async def stop_cmd(event):
            if self.harvesting:
                self.harvesting = False
                await event.reply("⚠️ Harvest stopped (current validation will finish).")
            else:
                await event.reply("No harvest in progress.")

        @self.client.on(events.NewMessage(pattern='/proxies'))
        async def list_proxies(event):
            proxies = get_working_proxies(limit=20)
            if not proxies:
                await event.reply("No working proxies. Run `/harvest` first.")
                return
            msg = "**Working Proxies (first 20):**\n```\n"
            for p in proxies:
                msg += f"{p['protocol']}://{p['proxy']}\n"
            msg += "```"
            await event.reply(msg)

        @self.client.on(events.NewMessage(pattern='/export_proxies'))
        async def export_cmd(event):
            proxies = get_working_proxies(limit=500)
            if not proxies:
                await event.reply("No proxies to export. Run `/harvest`.")
                return
            file_name = f"proxies_{int(time.time())}.txt"
            with open(file_name, "w") as f:
                for p in proxies:
                    f.write(f"{p['protocol']}://{p['proxy']}\n")
            await self.client.send_file(event.chat_id, file_name, caption="📦 Proxy list - one per line")
            os.remove(file_name)
            await event.reply(f"Exported {len(proxies)} proxies.")

        @self.client.on(events.NewMessage(pattern='/proxy_status'))
        async def status_cmd(event):
            count = get_proxy_count()
            await event.reply(f"📊 **Proxy Farm Status**\nWorking proxies: `{count}`\nLast harvest: use `/harvest` to refresh.")

        await self.client.run_until_disconnected()

async def main():
    print("="*50)
    print("DEDSEC PROXY FARM - Telegram Bot Edition")
    print("="*50)
    bot_token = input("Bot Token: ").strip()
    api_id = int(input("API ID: ").strip())
    api_hash = input("API Hash: ").strip()
    bot = ProxyFarmBot(api_id, api_hash, bot_token)
    await bot.start()

if __name__ == "__main__":
    asyncio.run(main())
