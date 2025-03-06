import os
import subprocess
import sys
import requests

# Function to create a buildozer.spec file
def create_buildozer_spec():
    spec_content = """
[app]

# (str) Title of your application
title = EthPrivateKeyViewer

# (str) Package name
package.name = eth_private_key_viewer

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source files
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
# List of dependencies required for your app to run.
# For kivy, you need to add kivy here. Other dependencies for your app (e.g., eth-account) can be added here as well.
# Example: requirements = sqlite3,python3,kivy
requirements = kivy,eth-account

# (list) Application source directories
# Add your project directory where eth_private_key_viewer.py is located
source.dir = .

# (str) Android NDK version to use (if you are using any native code)
# ndk = r19c

# (int) Android API to target (can be any API level like 28, 29, etc.)
android.api = 28

# (str) Android SDK version
android.sdk = 28

# (str) Android NDK version
android.ndk = 19b

# (bool) Debugging information
#debug = 1
"""
    
    with open("buildozer.spec", "w") as spec_file:
        spec_file.write(spec_content)
    print("buildozer.spec file created successfully.")


# Function to install buildozer and dependencies
def install_dependencies():
    print("Installing buildozer and dependencies...")
    subprocess.run(["pip", "install", "buildozer"], check=True)
    print("Buildozer installed successfully.")


# Function to run buildozer command to create APK
def create_apk():
    print("Starting APK creation process...")
    subprocess.run(["buildozer", "android", "debug"], check=True)
    print("APK created successfully.")


# Function to send the APK to Telegram
def send_apk_to_telegram(apk_file_path):
    bot_token = "your_telegram_bot_token"  # Replace with your Telegram Bot token
    chat_id = "your_telegram_chat_id"      # Replace with your Telegram Chat ID
    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"

    with open(apk_file_path, "rb") as apk_file:
        payload = {
            "chat_id": chat_id
        }
        files = {
            "document": apk_file
        }
        response = requests.post(url, data=payload, files=files)

    if response.status_code == 200:
        print(f"APK sent to Telegram chat {chat_id}.")
    else:
        print(f"Failed to send APK to Telegram. Status code: {response.status_code}")


# Main function
def main():
    if len(sys.argv) < 2:
        print("Usage: python create_apk.py <path-to-eth_private_key_viewer.py>")
        sys.exit(1)

    # Path to the eth_private_key_viewer.py file
    python_file_path = sys.argv[1]
    
    if not os.path.exists(python_file_path):
        print(f"Error: The file '{python_file_path}' does not exist.")
        sys.exit(1)

    # Create buildozer.spec file
    create_buildozer_spec()

    # Install buildozer and dependencies
    install_dependencies()

    # Run buildozer to create APK
    create_apk()

    # After APK is created, send it to Telegram
    apk_path = "bin/eth_private_key_viewer-debug.apk"  # Path to the generated APK
    send_apk_to_telegram(apk_path)


if __name__ == "__main__":
    main()
