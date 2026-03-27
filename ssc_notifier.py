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
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    notices = []
    
    # ⚠️ This selector may need adjustment later
    for a in soup.find_all("a"):
        text = a.text.strip()
        if text:
            notices.append(text)

    return notices[:20]  # limit to avoid spam

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

    updates = [n for n in new if n not in old]

    if updates:
        msg = "🚨 SSC New Updates:\n\n" + "\n".join(updates[:5])
        send_telegram(msg)

    save_new(new)

if __name__ == "__main__":
    main()
