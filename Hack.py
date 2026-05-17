import os
import sys
import time
import re
import telebot
import requests
from bs4 import BeautifulSoup

# --- DEDSEC SYSTEM VISUALS ---
PURPLE = "\033[95m"
CYAN = "\033[96m"
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

DEDSEC_BANNER = f"""
{PURPLE}
 ______   _______ ______   _______ _______ _______ 
 |     \\  |______ |     \\  |______ |______ |       
 |_____/  |______ |_____/  ______| |______ |_____  
                                                   
 [+] DESIGNATION: LEAKPROOF EXTRACTOR v3.0
 [+] STATUS: DNS COMPATIBLE // LOCALIZED SANDBOX
 [+] WARNING: DO NOT ACTIVATE GLOBAL VPN SESSIONS{RESET}
--------------------------------------------------
"""

def clear_terminal():
    os.system('clear')

def initialize_isolated_tor():
    """
    Spawns a strictly internal python-session routed via SOCKS5H.
    The 'h' extension forces DNS resolution to happen ON THE TOR NODE,
    preventing any leak from overriding your local iOS configuration.
    """
    session = requests.Session()
    session.proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    session.headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    return session

def main():
    clear_terminal()
    print(DEDSEC_BANNER)

    print(f"{CYAN}[!] ALERT: Booting isolated matrix...{RESET}")
    bot_token = input(f"{PURPLE}INPUT TG BOT TOKEN // {RESET}").strip()
    chat_id = input(f"{PURPLE}INPUT AUTH CHAT ID  // {RESET}").strip()

    if not bot_token or not chat_id:
        print(f"{RED}[!] ACCESS DENIED: Missing identity parameters.{RESET}")
        sys.exit(1)

    # Boot local session tunnel
    session = initialize_isolated_tor()

    try:
        print(f"{CYAN}[*] Sending ping through proxy pipeline...{RESET}")
        node_ip = session.get("https://api.ipify.org", timeout=12).text
        print(f"{GREEN}[+] SUCCESS. Internal Node IP verified: {node_ip}{RESET}")
        print(f"{GREEN}[+] iOS DNS profiles preserved. Certificate blockades secure.{RESET}\n")
    except Exception as network_err:
        print(f"{RED}[!] PIPELINE CRASHED: Tor engine not responding on port 9050.{RESET}")
        print(f"[*] Fix: Run 'tor &' in your iSH terminal before executing this matrix.")
        sys.exit(1)

    # Connect Telegram Interface
    bot = telebot.TeleBot(bot_token)
    print(f"{CYAN}[+] DedSec Daemon actively running in background...{RESET}")

    @bot.message_handler(commands=['start'])
    def handle_handshake(message):
        if str(message.chat.id) == chat_id:
            bot.reply_to(message, "⚡ 𝖣𝖤𝖣𝖲𝖤𝖢 𝖨𝖭𝖳𝖤𝖱𝖥𝖠𝖢𝖤: 𝖮𝖭𝖫𝖨𝖭𝖤 ⚡\nSend a codeword matrix asset to begin indexing.")

    @bot.message_handler(func=lambda message: True)
    def harvest_payload(message):
        if str(message.chat.id) != chat_id:
            return  # Firewall rogue users

        codeword = message.text.strip()
        bot.reply_to(message, f"🎮 Processing matrix index search for: '{codeword}'...")

        # Craft scraping URL targeting open source archives
        target_search = f"https://github.com/search?q={codeword}+language%3APython&type=code"
        indexed_files = []

        try:
            # Query web archive through isolated Tor node
            query_response = session.get(target_search, timeout=15)
            if query_response.status_code == 200:
                soup = BeautifulSoup(query_response.text, 'html.parser')
                links = soup.find_all('a', href=True)
                
                for link in links:
                    path_href = link['href']
                    # Pattern matching for raw code payloads
                    if '/blob/' in path_href and path_href.endswith('.py'):
                        raw_endpoint = "https://raw.githubusercontent.com" + path_href.replace('/blob/', '/')
                        file_identity = path_href.split('/')[-1]
                        indexed_files.append({'name': file_identity, 'url': raw_endpoint})
                        
                        if len(indexed_files) >= 3:  # Optimized buffer ceiling for mobile runtimes
                            break
        except Exception as query_fault:
            print(f"{RED}[!] Scraping failure inside matrix: {query_fault}{RESET}")

        if not indexed_files:
            bot.send_message(chat_id, "❌ Zero matches found, or target network actively dropped our sequence.")
            return

        bot.send_message(chat_id, f"👾 Index match verified! Transporting {len(indexed_files)} scripts across encrypted channel...")

        for asset in indexed_files:
            try:
                # Direct down-stream capture through proxy loop
                raw_payload_data = session.get(asset['url'], timeout=10).content
                runtime_filename = f"dedsec_{asset['name']}"

                # Drop transient file onto iSH virtual sandbox disk
                with open(runtime_filename, 'wb') as output_buffer:
                    output_buffer.write(raw_payload_data)

                # Transmit file to the control room
                with open(runtime_filename, 'rb') as control_upload:
                    bot.send_document(chat_id, control_upload, caption=f"🛰️ Source Node: {asset['url']}")

                # Vaporize trace assets off the drive immediately
                os.remove(runtime_filename)
                time.sleep(2)  # Delay prevents transmission alerts on Telegram nodes

            except Exception as transfer_fault:
                bot.send_message(chat_id, f"⚠️ Transmission packet drop for {asset['name']}: {str(transfer_fault)}")

    try:
        bot.polling(none_stop=True)
    except KeyboardInterrupt:
        print(f"\n{RED}[-] SYSTEM OFFLINE: Script sequence killed by operator.{RESET}")

if __name__ == "__main__":
    main()
