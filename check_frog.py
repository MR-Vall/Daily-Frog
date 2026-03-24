import instaloader
import requests
import json
import os

INSTAGRAM_USER = "frogpicturesdaily"
DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]
INSTAGRAM_USERNAME = os.environ["INSTAGRAM_USER"]
INSTAGRAM_PASSWORD = os.environ["INSTAGRAM_PASS"]
LAST_POST_FILE = "last_post.json"


def load_last_shortcode():
    if os.path.exists(LAST_POST_FILE):
        with open(LAST_POST_FILE) as f:
            return json.load(f).get("last_shortcode")
    return None


def save_last_shortcode(shortcode):
    with open(LAST_POST_FILE, "w") as f:
        json.dump({"last_shortcode": shortcode}, f)


def send_to_discord(post):
    caption = post.caption[:300] if post.caption else ""
    payload = {
        "embeds": [
            {
                "title": "🐸 Daily Frog!",
                "description": caption,
                "image": {"url": post.url},
                "url": f"https://www.instagram.com/p/{post.shortcode}/",
                "color": 0x57F287,
                "footer": {"text": f"@{INSTAGRAM_USER} on Instagram"},
            }
        ]
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    response.raise_for_status()
    print(f"Posted to Discord: {post.shortcode}")


def main():
    L = instaloader.Instaloader()
    L.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
    profile = instaloader.Profile.from_username(L.context, INSTAGRAM_USER)

    last_shortcode = load_last_shortcode()

    # Get the latest post
    latest_post = next(iter(profile.get_posts()), None)

    if latest_post is None:
        print("No posts found.")
        return

    if latest_post.shortcode == last_shortcode:
        print("No new posts since last run.")
        return

    send_to_discord(latest_post)
    save_last_shortcode(latest_post.shortcode)


if __name__ == "__main__":
    main()
