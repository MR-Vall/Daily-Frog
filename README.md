# 🐸 Daily Frog Discord Bot
 
Automatically posts frog pictures to a Discord channel every day via a webhook. Pulls from both [@frogpicturesdaily](https://www.instagram.com/frogpicturesdaily/) on Instagram and [@frogofthe](https://x.com/frogofthe) on X, working through posts oldest to newest. Runs entirely on GitHub Actions — no server or PC required.
 
---
 
## How it works
 
A GitHub Actions workflow runs once a day on a schedule. It reads both RSS feeds, merges all posts sorted oldest to newest, and sends the next one in the queue to your Discord channel as an embed. The footer of each post shows which account it came from. If all posts have been sent it waits until new ones appear.
 
No Instagram or X account required.
 
---
 
## Setup
 
### 1. Fork or clone this repo
 
Create a new GitHub repository and add the files:
 
```
check_frog.py
.github/workflows/frog.yml
```
 
### 2. Create a Discord webhook
 
1. Open Discord and go to the channel you want frogs in
2. Click **Edit Channel → Integrations → Webhooks → New Webhook**
3. Give it a name (e.g. "Frog Bot") and copy the webhook URL
 
> 💡 Webhooks only work in server channels, not DMs. If you want it to feel private, create a personal Discord server just for yourself.
 
### 3. Add the webhook URL as a GitHub secret
 
1. In your GitHub repo, go to **Settings → Secrets and variables → Actions**
2. Click **New repository secret**
3. Name: `DISCORD_WEBHOOK_URL`
4. Value: paste your webhook URL
 
### 4. Done
 
The bot will now run automatically every day at **9:00 AM UTC (10:00 AM Copenhagen time)**. You can also trigger it manually at any time from the **Actions** tab in your repo by clicking **Run workflow**.
 
---
 
## Files
 
| File | Description |
|------|-------------|
| `check_frog.py` | Reads both RSS feeds and posts the next frog in the queue to Discord |
| `.github/workflows/frog.yml` | GitHub Actions workflow that runs the script daily |
| `last_post.json` | Auto-generated — tracks the last posted photo to avoid duplicates |
 
---
 
## Sources
 
| Account | Platform | RSS Feed |
|---------|----------|----------|
| @frogpicturesdaily | Instagram | `https://rss.app/feeds/rCucomTDdY1cFJtG.xml` |
| @frogofthe | X | `https://rss.app/feeds/FSqpCA2JxIi20sHt.xml` |
 
RSS feeds are provided by [rss.app](https://rss.app). To add more sources, create a new feed on rss.app and add the XML URL to the `RSS_FEEDS` list in `check_frog.py`.
 
---
 
## Changing the schedule
 
The schedule is set in `frog.yml`:
 
```yaml
- cron: '0 9 * * *'  # Every day at 9:00 AM UTC (10:00 AM Copenhagen)
```
 
Use [crontab.guru](https://crontab.guru) to help write a different schedule if needed.
 
---
 
## Dependencies
 
Installed automatically by the workflow — nothing to install manually.
 
- [requests](https://requests.readthedocs.io/) — fetches the RSS feeds and sends the Discord webhook
 
---
 
## Notes
 
- Posts are worked through oldest to newest across both sources, one per day.
- The Discord embed footer shows which account each frog came from.
- The script only posts one frog per day and never posts duplicates.
- Webhooks can only post to server channels, not Discord DMs. If you want it to feel private, create a personal Discord server and point the webhook there.
