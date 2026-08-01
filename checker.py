import os
import random
import string
import time
import requests

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
CHOICE = os.getenv("USER_CHOICE", "4l").strip().lower()
AMOUNT = int(os.getenv("USER_AMOUNT", "5"))
CUSTOM_LENGTH = int(os.getenv("CUSTOM_LENGTH", "4"))

GITHUB_API_URL = "https://api.github.com/users/{}"
HEADERS = {"User-Agent": "GitHub-Handle-Checker/1.0"}

REAL_WORDS = [
    "spark", "vivid", "orbit", "cloud", "pixel", "stone", "amber",
    "breeze", "shadow", "summit", "drift", "pulse", "frost", "blaze",
    "echo", "prism", "solar", "matrix", "vertex", "vector", "atlas"
]

def generate_usernames(choice, count, custom_len):
    letters = string.ascii_lowercase
    alphanumeric = string.ascii_lowercase + string.digits

    preset_map = {
        "2l": (2, letters),      "2c": (2, alphanumeric),
        "3l": (3, letters),      "3c": (3, alphanumeric),
        "4l": (4, letters),      "4c": (4, alphanumeric),
        "5l": (5, letters),      "5c": (5, alphanumeric),
    }

    results = []

    if choice in preset_map:
        length, pool = preset_map[choice]
        for _ in range(count):
            results.append("".join(random.choices(pool, k=length)))

    elif choice == "custom":
        for _ in range(count):
            results.append("".join(random.choices(alphanumeric, k=custom_len)))

    elif choice == "words":
        for _ in range(count):
            results.append(random.choice(REAL_WORDS))

    return results

def check_github_username(username):
    url = GITHUB_API_URL.format(username)
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
        if response.status_code == 404:
            return "AVAILABLE"
        elif response.status_code == 200:
            return "TAKEN"
        elif response.status_code == 429:
            return "RATE LIMITED"
        else:
            return f"UNKNOWN ({response.status_code})"
    except requests.RequestException:
        return "ERROR"

def send_to_discord(username):
    if not DISCORD_WEBHOOK_URL:
        return

    payload = {
        "username": "GitHub Handle Checker",
        "embeds": [{
            "title": "🎉 Username Available!",
            "description": f"The handle **`{username}`** is available on **GitHub**!",
            "url": f"https://github.com/{username}",
            "color": 3066993,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }]
    }

    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)
        print(f"  [+] Discord alert sent for '{username}'")
    except requests.RequestException:
        pass

def main():
    print(f"=== MOBILE GITHUB ACTION CHECKER ===")
    print(f"Option: {CHOICE} | Amount: {AMOUNT} | Custom Len: {CUSTOM_LENGTH}\n")

    usernames = generate_usernames(CHOICE, AMOUNT, CUSTOM_LENGTH)

    for name in usernames:
        status = check_github_username(name)
        print(f"'{name:<12}' -> {status}")

        if status == "AVAILABLE":
            send_to_discord(name)

        time.sleep(1)

if __name__ == "__main__":
    main()
