import os
import subprocess
import base64

MAIN_SCRIPT_PATH = "main.py"
BUILT_SCRIPT_PATH = "built_main.py"

def get_input_from_user():
    
    token = input("Enter your bot token: ")
    webhook_url = input("Enter your webhook URL: ")
    return token, webhook_url

def encode_values(token, webhook_url):
    
    encoded_token = base64.b64encode(token.encode('utf-8')).decode('utf-8')
    encoded_webhook_url = base64.b64encode(webhook_url.encode('utf-8')).decode('utf-8')
    return encoded_token, encoded_webhook_url

def build_script():
    # Get token and webhook from the user
    token, webhook_url = get_input_from_user()

    
    encoded_token, encoded_webhook_url = encode_values(token, webhook_url)

    
    if not os.path.exists(MAIN_SCRIPT_PATH):
        print(f"❌ Error: {MAIN_SCRIPT_PATH} not found!")
        return

    with open(MAIN_SCRIPT_PATH, "r", encoding="utf-8") as file:
        script_content = file.read()

    
    decode_part = f"""
import base64


encoded_token = '{encoded_token}'
encoded_webhook_url = '{encoded_webhook_url}'


TOKEN = base64.b64decode(encoded_token).decode('utf-8')
WEBHOOK_URL = base64.b64decode(encoded_webhook_url).decode('utf-8')


"""

    
    built_script_content = decode_part + "\n" + script_content

    
    with open(BUILT_SCRIPT_PATH, "w", encoding="utf-8") as file:
        file.write(built_script_content)

    print(f"✅ Built script saved as {BUILT_SCRIPT_PATH}")
    print("Opening YouTube tutorial for PyInstaller...")

    youtube_link = "https://youtu.be/2X9rxzZbYqg?si=E4U_ooHl8Q_YiIPK"
    subprocess.run(["python", "-m", "webbrowser", youtube_link])

if __name__ == "__main__":
    build_script()
