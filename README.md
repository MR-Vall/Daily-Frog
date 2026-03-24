# 🐸 Daily Frog Discord Bot
 
Automatically posts the latest photo from [@frogpicturesdaily](https://www.instagram.com/frogpicturesdaily/) to a Discord channel every day via a webhook. Runs entirely on GitHub Actions — no server or PC required.
 
---
 
## How it works
 
A GitHub Actions workflow runs once a day on a schedule. It fetches the latest post from the Instagram profile and sends it to your Discord channel as an embed. If there's no new post since the last run, it does nothing.
 
---
 
## Setup
 
### 1. Fork or clone this repo
 
Create a new GitHub repository and add the two files:
 
```
check_frog.py
.github/workflows/frog.yml
```
 
### 2. Create a Discord webhook
 
1. Open Discord and go to the channel you want frogs in
2. Click **Edit Channel → Integrations → Webhooks → New Webhook**
3. Give it a name (e.g. "Frog Bot") and copy the webhook URL
 
### 3. Add the webhook URL as a GitHub secret
 
1. In your GitHub repo, go to **Settings → Secrets and variables → Actions**
2. Click **New repository secret**
3. Name: `DISCORD_WEBHOOK_URL`
4. Value: paste your webhook URL
 
### 4. Done
 
The bot will now run automatically every day at **9:00 AM UTC**. You can also trigger it manually at any time from the **Actions** tab in your repo by clicking **Run workflow**.
 
---
 
## Files
 
| File | Description |
|------|-------------|
| `check_frog.py` | Fetches the latest Instagram post and sends it to Discord |
| `.github/workflows/frog.yml` | GitHub Actions workflow that runs the script daily |
| `last_post.json` | Auto-generated — tracks the last posted photo to avoid duplicates |
 
---
 
## Changing the schedule
 
The schedule is set in `frog.yml`:
 
```yaml
- cron: '0 9 * * *'  # Every day at 9:00 AM UTC
```
 
Use [crontab.guru](https://crontab.guru) to help write a different schedule if needed.
 
---
 
## Dependencies
 
Installed automatically by the workflow — nothing to install manually.
 
- [instaloader](https://instaloader.github.io/) — fetches Instagram posts
- [requests](https://requests.readthedocs.io/) — sends the Discord webhook
 
---
 
## Notes
 
- This uses `instaloader` to fetch public Instagram posts. It does not require an Instagram account.
- The script only posts once per day even if the workflow runs multiple times.
- Webhooks can only post to server channels, not Discord DMs. If you want it to feel private, create a personal Discord server and point the webhook there.
