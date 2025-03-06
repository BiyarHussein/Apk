import os
import requests

def send_apk_to_telegram(apk_file_path):
    bot_token = "2006365451:AAGloQmFGgdjL_NkhAnQ6T3Ohrt1hXtLfRU"  # Replace with your Telegram Bot token
    chat_id = "903017073"      # Replace with your Telegram Chat ID
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


# Example usage
apk_file_path = "bin/eth_private_key_viewer-debug.apk"  # Path to the generated APK
send_apk_to_telegram(apk_file_path)
