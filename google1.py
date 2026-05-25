#!/usr/bin/env python3
"""
DEDSEC GOOGLE FACTORY v1.0
===========================
Creates Google accounts without phone numbers.
Uses: clean residential proxies, cookie warming, Android flow simulation.
"""

import asyncio, random, time, os, json, re, sqlite3
from datetime import datetime
from playwright.async_api import async_playwright
from cryptography.fernet import Fernet

class GoogleFactory:
    def __init__(self, proxy_list, master_pass):
        self.proxies = proxy_list
        self.key = base64.urlsafe_b64encode(
            hashlib.pbkdf2_hmac('sha256', master_pass.encode(), b'googlesalt', 100000)
        )[:32]
        self.cipher = Fernet(self.key)
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect('google_vault.db')
        conn.execute('''CREATE TABLE IF NOT EXISTS accounts
            (id INTEGER PRIMARY KEY, email TEXT, password TEXT, created TEXT)''')
        conn.commit(); conn.close()

    def save(self, email, password):
        conn = sqlite3.connect('google_vault.db')
        conn.execute("INSERT INTO accounts (email, password, created) VALUES (?,?,?)",
                     (email, self.cipher.encrypt(password.encode()).decode(), datetime.now().isoformat()))
        conn.commit(); conn.close()

    async def create_account(self, first, last, username, password):
        """Attempt 1: Clean browser with residential proxy. If Skip appears, we win."""
        
        async with async_playwright() as p:
            proxy = random.choice(self.proxies)
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context(
                user_agent=random.choice(UA_LIST),
                viewport={"width": random.randint(1280,1440), "height": random.randint(720,900)},
                locale="en-US",
                proxy={"server": proxy}
            )
            page = await context.new_page()

            try:
                await page.goto("https://accounts.google.com/signup", timeout=30000)
                await asyncio.sleep(random.uniform(2,4))
                
                # Fill name
                await page.fill('input[name="firstName"]', first)
                await asyncio.sleep(random.uniform(0.5,1.5))
                await page.fill('input[name="lastName"]', last)
                await asyncio.sleep(random.uniform(0.5,1.5))
                await page.click('#next')
                await asyncio.sleep(random.uniform(2,4))

                # Try Method 3: Use existing email instead of Gmail
                await page.click('button:has-text("Use your existing email")')
                await asyncio.sleep(random.uniform(1,2))
                
                # Enter existing email (we'll use a temp one)
                temp_email = f"{username}@outlook.com"
                await page.fill('input[type="email"]', temp_email)
                await asyncio.sleep(random.uniform(0.5,1))
                await page.click('#next')
                await asyncio.sleep(random.uniform(2,4))

                # Fill password
                await page.fill('input[name="password"]', password)
                await asyncio.sleep(random.uniform(0.5,1))
                await page.fill('input[name="confirmPassword"]', password)
                await asyncio.sleep(random.uniform(0.5,1))
                await page.click('#next')
                await asyncio.sleep(random.uniform(2,4))

                # Birthday
                await page.fill('input[name="day"]', str(random.randint(1,28)))
                await page.select_option('select[name="month"]', str(random.randint(1,12)))
                await page.fill('input[name="year"]', str(random.randint(1980,2000)))
                await page.select_option('select[name="gender"]', random.choice(['1','2','3','4']))
                await page.click('#next')
                await asyncio.sleep(random.uniform(2,4))

                # Phone screen — look for Skip
                skip_btn = await page.query_selector('button:has-text("Skip")')
                if skip_btn:
                    await skip_btn.click()
                    await asyncio.sleep(random.uniform(2,4))
                    
                    # Terms
                    await page.click('button:has-text("I agree")')
                    await asyncio.sleep(3)
                    
                    self.save(temp_email, password)
                    await browser.close()
                    return {"ok": True, "email": temp_email, "password": password}
                
                # If no Skip, try Method 2: Pretend we're on Android
                await browser.close()
                return await self.android_method(first, last, username, password)

            except Exception as e:
                await browser.close()
                return {"ok": False, "error": str(e)}

    async def android_method(self, first, last, username, password):
        """Method 2: Simulate Android Settings → Add Account flow."""
        # This requires an Android emulator with ADB or a cloud phone.
        # For automated web simulation, we use the Android user agent + specific headers.
        
        async with async_playwright() as p:
            proxy = random.choice(self.proxies)
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36",
                viewport={"width": 412, "height": 915},
                locale="en-US",
                is_mobile=True,
                has_touch=True,
                proxy={"server": proxy}
            )
            page = await context.new_page()

            try:
                # Use the Google Signup page with mobile parameters
                await page.goto("https://accounts.google.com/signup/v2/webcreateaccount?flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S-123456&theme=glif&TL=AE-bA-w6", timeout=30000)
                await asyncio.sleep(random.uniform(3,5))

                await page.fill('input[name="firstName"]', first)
                await asyncio.sleep(random.uniform(1,2))
                await page.click('button:has-text("Next")')
                await asyncio.sleep(random.uniform(2,4))

                # Use email creation
                await page.click('button:has-text("Create your Gmail")')
                await asyncio.sleep(random.uniform(1,2))

                # Enter desired username
                await page.fill('input[name="username"]', username)
                await asyncio.sleep(random.uniform(0.5,1))
                await page.click('button:has-text("Next")')
                await asyncio.sleep(random.uniform(2,4))

                # Password
                await page.fill('input[name="password"]', password)
                await page.fill('input[name="confirmPassword"]', password)
                await page.click('button:has-text("Next")')
                await asyncio.sleep(random.uniform(2,4))

                # Birthday + gender
                await page.select_option('select[name="month"]', str(random.randint(1,12)))
                await page.fill('input[name="day"]', str(random.randint(1,28)))
                await page.fill('input[name="year"]', str(random.randint(1980,2000)))
                await page.select_option('select[name="gender"]', random.choice(['1','2','3','4']))
                await page.click('button:has-text("Next")')
                await asyncio.sleep(random.uniform(2,4))

                # Phone screen
                skip_btn = await page.query_selector('button:has-text("Skip")')
                if skip_btn:
                    await skip_btn.click()
                    await asyncio.sleep(random.uniform(2,4))
                    await page.click('button:has-text("I agree")')
                    await asyncio.sleep(3)
                    email = f"{username}@gmail.com"
                    self.save(email, password)
                    await browser.close()
                    return {"ok": True, "email": email, "password": password}
                
                await browser.close()
                return {"ok": False, "error": "Phone required, no Skip button"}

            except Exception as e:
                await browser.close()
                return {"ok": False, "error": str(e)}

UA_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 Chrome/124.0.6367.113 Mobile Safari/537.36",
]

if __name__ == "__main__":
    import base64, hashlib
    print("DEDSEC GOOGLE FACTORY")
    master = input("Master password: ").strip()
    proxies = []
    if os.path.exists("proxies.txt"):
        with open("proxies.txt") as f:
            proxies = [l.strip() for l in f if l.strip()]
    if not proxies:
        print("No proxies. Add residential proxies to proxies.txt")
        sys.exit(1)

    factory = GoogleFactory(proxies, master)
    
    first = input("First name: ").strip()
    last = input("Last name: ").strip()
    user = input("Desired username: ").strip()
    pwd = input("Password: ").strip()
    
    result = asyncio.run(factory.create_account(first, last, user, pwd))
    print(json.dumps(result, indent=2))
