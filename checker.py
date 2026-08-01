import os
import random
import string
import time
import requests

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
CHOICE = os.getenv("USER_CHOICE", "4l").strip().lower()
AMOUNT = int(os.getenv("USER_AMOUNT", "5"))
CUSTOM_LENGTH = int(os.getenv("CUSTOM_LENGTH", "4"))

# AI-style word components
PREFIXES = [
    "hyper", "cyber", "omni", "neo", "retro", "meta", "crypto", "astro",
    "ultra", "super", "micro", "macro", "proto", "synth", "techno", "zen"
]

ROOT_WORDS = [
    "spark", "vivid", "orbit", "cloud", "pixel", "stone", "amber", "breeze",
    "shadow", "summit", "drift", "pulse", "frost", "blaze", "echo", "prism",
    "solar", "matrix", "vertex", "vector", "atlas", "lunar", "nova", "shift",
    "vault", "nexus", "surge", "bloom", "forge", "craft", "realm"
]

SUFFIXES = [
    "lab", "hub", "io", "hq", "sys", "tech", "box", "flow", "mind", "wave",
    "core", "net", "sync", "bot", "base", "grid", "verse", "link", "craft"
]


def generate_ai_words(count):
    generated = set()
    while len(generated) < count:
        pattern = random.choice([1, 2, 3])
        if pattern == 1:
            word = random.choice(PREFIXES) + random.choice(ROOT_WORDS)
        elif pattern == 2:
            word = random.choice(ROOT_WORDS) + random.choice(SUFFIXES)
        else:
            word1, word2 = random.sample(ROOT_WORDS, 2)
            word = word1 + word2
        generated.add(word)
    return list(generated)


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
        results = generate_ai_words(count)

    return results


def send_to_discord(handles, choice_type):
    if not DISCORD_WEBHOOK_URL:
        print("[!] No Discord Webhook URL provided.")
        return

    # Formats handles into a clean bulleted list for Discord
    handle_list = "\n".join([f"• `{h}`" for h in handles])

    payload = {
        "username": "Discord Handle Generator",
        "embeds": [{
            "title": f"🎲 Generated Discord Handles ({choice_type.upper()})",
            "description": f"Here are your generated handles to test on Discord:\n\n{handle_list}",
            "color": 5814783,  # Discord Blurple Color
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }]
    }

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)
        if response.status_code in [200, 204]:
            print(f"[+] Sent {len(handles)} handles to Discord!")
        else:
            print(f"[!] Webhook error status: {response.status_code}")
    except requests.RequestException as e:
        print(f"[!] Failed to send webhook: {e}")


def main():
    print("=== DISCORD HANDLE GENERATOR ===")
    print(f"Option: {CHOICE} | Amount: {AMOUNT} | Custom Len: {CUSTOM_LENGTH}\n")

    usernames = generate_usernames(CHOICE, AMOUNT, CUSTOM_LENGTH)
    
    print("Generated Handles:")
    for u in usernames:
        print(f" - {u}")

    send_to_discord(usernames, CHOICE)


if __name__ == "__main__":
    main()
