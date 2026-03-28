import requests
from bs4 import BeautifulSoup
import json
import os

URL = "https://ssc.gov.in/home/notice-board"

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

    try:
        response = requests.get(URL, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print("ERROR:", e)
        return []

    print("STATUS CODE:", response.status_code)
    print("PAGE LENGTH:", len(response.text))

    soup = BeautifulSoup(response.text, "html.parser")

    notices = []

    for a in soup.find_all("a"):
        text = a.text.strip()
        if text:
            notices.append(text)

    print("FOUND NOTICES:", len(notices))

    return notices[:20]

def load_old():
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            return json.load(f)
    return []

def save_new(data):
    import subprocess
    import json

    with open("data.json", "w") as f:
        json.dump(data, f)

    # Configure git
    subprocess.run(["git", "config", "--global", "user.email", "bot@example.com"])
    subprocess.run(["git", "config", "--global", "user.name", "github-actions"])

    # Add & commit only if changes exist
    subprocess.run(["git", "add", "data.json"])
    subprocess.run(["git", "commit", "-m", "Update data"], check=False)
    subprocess.run(["git", "push"])

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
 
