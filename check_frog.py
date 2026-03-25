import requests
import json
import os
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
 
RSS_FEEDS = [
    "https://rss.app/feeds/rCucomTDdY1cFJtG.xml",  # Instagram @frogpicturesdaily
    "https://rss.app/feeds/FSqpCA2JxIi20sHt.xml",   # X @frogofthe
]
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
    namespaces = {'media': 'http://search.yahoo.com/mrss/'}
    media = item.find('media:content', namespaces)
    if media is not None:
        return media.get('url')
 
    enclosure = item.find('enclosure')
    if enclosure is not None:
        return enclosure.get('url')
 
    description = item.findtext('description') or ''
    if 'img src=' in description:
        start = description.find('img src="') + 9
        end = description.find('"', start)
        if start > 9 and end > start:
            return description[start:end]
 
    return None
 
 
def get_pub_date(item):
    pub_date = item.findtext('pubDate')
    if pub_date:
        try:
            return parsedate_to_datetime(pub_date)
        except Exception:
            pass
    return None
 
 
def fetch_all_items():
    all_items = []
    for feed_url in RSS_FEEDS:
        try:
            response = requests.get(feed_url, timeout=10)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            channel = root.find('channel')
            items = channel.findall('item')
            all_items.extend(items)
            print(f"Fetched {len(items)} items from {feed_url}")
        except Exception as e:
            print(f"Failed to fetch {feed_url}: {e}")
 
    # Sort all items oldest to newest by pubDate
    all_items.sort(key=lambda x: get_pub_date(x) or 0)
    return all_items
 
 
def send_to_discord(title, image_url, link, source):
    payload = {
        "embeds": [
            {
                "title": "🐸 Daily Frog!",
                "description": title,
                "image": {"url": image_url},
                "url": link,
                "color": 0x57F287,
                "footer": {"text": source},
            }
        ]
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    response.raise_for_status()
    print(f"Posted to Discord: {title}")
 
 
def get_source_label(link):
    if 'instagram.com' in link:
        return '@frogpicturesdaily on Instagram'
    elif 'x.com' in link or 'twitter.com' in link:
        return '@frogofthe on X'
    return 'Daily Frog'
 
 
def main():
    items = fetch_all_items()
 
    if not items:
        print("No items found in any feed.")
        return
 
    last_guid = load_last_guid()
 
    next_item = None
    if last_guid is None:
        next_item = items[0]
    else:
        for i, item in enumerate(items):
            guid = item.findtext('guid') or item.findtext('link')
            if guid == last_guid:
                if i + 1 < len(items):
                    next_item = items[i + 1]
                else:
                    print("All posts have been sent, waiting for new ones.")
                    return
                break
 
    if next_item is None:
        next_item = items[0]
 
    guid = next_item.findtext('guid') or next_item.findtext('link')
    title = next_item.findtext('title') or "New post"
    link = next_item.findtext('link') or ""
    image_url = get_image_from_item(next_item)
    source = get_source_label(link)
 
    if not image_url:
        print("No image found in post, skipping.")
        save_last_guid(guid)
        return
 
    send_to_discord(title, image_url, link, source)
    save_last_guid(guid)
 
 
if __name__ == "__main__":
    main()
