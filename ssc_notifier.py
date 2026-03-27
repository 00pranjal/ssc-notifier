import requests
from bs4 import BeautifulSoup
import json
import os

URL = "https://ssc.gov.in"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)

def get_notices():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for _ in range(3):  # retry 3 times
        try:
            response = requests.get(URL, headers=headers, timeout=10)
            response.raise_for_status()
            break
        except requests.exceptions.RequestException:
            continue
    else:
        return []  # if all retries fail

    soup = BeautifulSoup(response.text, "html.parser")

    notices = []
    for a in soup.find_all("a"):
        text = a.text.strip()
        if text:
            notices.append(text)

    return notices[:20]

def load_old():
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            return json.load(f)
    return []

def save_new(data):
    with open("data.json", "w") as f:
        json.dump(data, f)

def main():
    old = load_old()
    new = get_notices()

    if not old:
        send_telegram("✅ SSC Notifier started successfully!")
    
    updates = [n for n in new if n not in old]

    if updates:
        msg = "🚨 SSC New Updates:\n\n" + "\n".join(updates[:5])
        send_telegram(msg)

    save_new(new)

if __name__ == "__main__":
    main()
