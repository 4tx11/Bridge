# -*- coding: utf-8 -*-
import marshal
import re
import ast
import requests
import time
import base64
import zlib
import os

# --- CONFIGURATION ---
print("--- Telegram Bot Configuration ---")
BOT_TOKEN = input("[?] Enter your Telegram Bot Token: ").strip()

def deep_unpack(content):
    """Recursively unpacks layers of Base64, Zlib, and Marshal."""
    found_something = False
    current_content = content

    # 1. Try to find and decode Base64 layers
    b64_match = re.search(r'base64\.b64decode\([\'"](.+?)[\'"]\)', current_content)
    if b64_match:
        try:
            current_content = base64.b64decode(b64_match.group(1)).decode('utf-8', errors='ignore')
            found_something = True
        except: pass

    # 2. Try to find and decompress Zlib layers
    zlib_match = re.search(r'zlib\.decompress\([\'"](.+?)[\'"]\)', current_content)
    if zlib_match:
        try:
            zlib_data = ast.literal_eval(zlib_match.group(1))
            current_content = zlib.decompress(zlib_data).decode('utf-8', errors='ignore')
            found_something = True
        except: pass

    # 3. Look for Marshal data
    marshal_match = re.search(r'marshal\.loads\(\s*(b[\'"].*?[\'"])\s*\)', current_content, re.DOTALL)
    if marshal_match:
        try:
            data_bytes = ast.literal_eval(marshal_match.group(1))
            code_obj = marshal.loads(data_bytes)
            
            output = "# --- DECRYPTED CONSTANTS ---\n"
            for const in code_obj.co_consts:
                if const is not None:
                    output += f"{repr(const)}\n"
            return output
        except Exception as e:
            return f"[-] Marshal Error: {str(e)}"

    # If we decoded a layer, try again on the new content
    if found_something:
        return deep_unpack(current_content)
    
    return current_content if len(current_content) > 0 else "[-] No recognizable encryption found."

def handle_telegram_updates():
    offset = 0
    print("\n[!] Bot is ONLINE. Send your .py files to the bot...")
    
    while True:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={offset}&timeout=30"
            response = requests.get(url).json()

            if "result" in response:
                for update in response["result"]:
                    offset = update["update_id"] + 1
                    message = update.get("message", {})
                    chat_id = message.get("chat", {}).get("id")
                    
                    if "document" in message:
                        file_name = message["document"]["file_name"]
                        file_id = message["document"]["file_id"]
                        print(f"[*] Processing file: {file_name}")

                        # Get file path
                        get_file = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}").json()
                        if "result" in get_file:
                            file_path = get_file["result"]["file_path"]
                            download_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
                            
                            # Download file content
                            file_data = requests.get(download_url).text
                            
                            # RUN DECRYPTION
                            decrypted_result = deep_unpack(file_data)
                            
                            # Save result to a file
                            output_file = f"decrypted_{file_name}"
                            with open(output_file, "w", encoding="utf-8") as f:
                                f.write(decrypted_result)
                            
                            # Send back to user
                            with open(output_file, "rb") as f:
                                requests.post(
                                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument",
                                    data={"chat_id": chat_id, "caption": "Done! File Decrypted."},
                                    files={"document": f}
                                )
                            print(f"[+] Sent results to Chat ID: {chat_id}")
                            if os.path.exists(output_file):
                                os.remove(output_file)

        except Exception as e:
            print(f"[-] Loop Error: {str(e)}")
            time.sleep(2)

if __name__ == "__main__":
    if not BOT_TOKEN:
        print("[-] Error: BOT_TOKEN is missing!")
    else:
        handle_telegram_updates()
