import os
import subprocess

MAIN_SCRIPT_PATH = "main.py"
BUILT_SCRIPT_PATH = "built_main.py"

def get_input_from_user():
    token = input("Enter your bot token: ")
    webhook_url = input("Enter your webhook URL: ")
    return token, webhook_url

def build_script():
    if not os.path.exists(MAIN_SCRIPT_PATH):
        print(f"❌ Error: {MAIN_SCRIPT_PATH} not found!")
        return

    token, webhook_url = get_input_from_user()

    with open(MAIN_SCRIPT_PATH, "r", encoding="utf-8") as file:
        script_content = file.read()

    script_content = script_content.replace("TOKEN = 'sex'", f"TOKEN = '{token}'")
    script_content = script_content.replace("WEBHOOK_URL = 'sex'", f"WEBHOOK_URL = '{webhook_url}'")

    with open(BUILT_SCRIPT_PATH, "w", encoding="utf-8") as file:
        file.write(script_content)

    print(f"✅ Built script saved as {BUILT_SCRIPT_PATH}")
    print("Opening YouTube tutorial for PyInstaller...")

    
    youtube_link = "https://youtu.be/2X9rxzZbYqg?si=E4U_ooHl8Q_YiIPK"  
    subprocess.run(["python", "-m", "webbrowser", youtube_link])

if __name__ == "__main__":
    build_script()
