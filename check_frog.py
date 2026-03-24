import requests
import json
import os
import xml.etree.ElementTree as ET
 
RSS_FEED_URL = "https://rss.app/feeds/rCucomTDdY1cFJtG.xml"
DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]
LAST_POST_FILE = "last_post.json"
 
 
def load_last_guid():
    if os.path.exists(LAST_POST_FILE):
        with open(LAST_POST_FILE) as f:
            return json.load(f).get("last_guid")
    return None
 
 
def save_last_guid(guid):
    with open(LAST_POST_FILE, "w") as f:
        json.dump({"last_guid": guid}, f)
 
 
def get_image_from_item(item):
    # Try media:content tag first
    namespaces = {
        'media': 'http://search.yahoo.com/mrss/',
    }
    media = item.find('media:content', namespaces)
    if media is not None:
        return media.get('url')
 
    # Try enclosure tag
    enclosure = item.find('enclosure')
    if enclosure is not None:
        return enclosure.get('url')
 
    # Try to find image URL in description
    description = item.findtext('description') or ''
    if 'img src=' in description:
        start = description.find('img src="') + 9
        end = description.find('"', start)
        if start > 9 and end > start:
            return description[start:end]
 
    return None
 
 
def send_to_discord(title, image_url, link):
    payload = {
        "embeds": [
            {
                "title": "🐸 Daily Frog!",
                "description": title,
                "image": {"url": image_url},
                "url": link,
                "color": 0x57F287,
                "footer": {"text": "@frogpicturesdaily on Instagram"},
            }
        ]
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    response.raise_for_status()
    print(f"Posted to Discord: {title}")
 
 
def main():
    response = requests.get(RSS_FEED_URL)
    response.raise_for_status()
 
    root = ET.fromstring(response.content)
    channel = root.find('channel')
    items = channel.findall('item')
 
    if not items:
        print("No items found in feed.")
        return
 
    latest = items[0]
    guid = latest.findtext('guid') or latest.findtext('link')
    title = latest.findtext('title') or "New post"
    link = latest.findtext('link') or ""
    image_url = get_image_from_item(latest)
 
    last_guid = load_last_guid()
 
    if guid == last_guid:
        print("No new posts since last run.")
        return
 
    if not image_url:
        print("No image found in latest post, skipping.")
        save_last_guid(guid)
        return
 
    send_to_discord(title, image_url, link)
    save_last_guid(guid)
 
 
if __name__ == "__main__":
    main()
