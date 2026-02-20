# 📺 KidWatch — YouTube Activity Tracker

A live dashboard tracking YouTube watch history — updated daily.

**Live Dashboard:** https://appforgelabs.github.io/KidWatch

## What It Shows
- Videos watched in the last 7 days
- Top channels and content categories
- Watch activity by hour and day of week
- Full recent video list with timestamps

## How It Works
1. Daily cron (8 PM ET) logs into YouTube via browser automation
2. Scrapes watch history from `youtube.com/feed/history`
3. Categorizes videos by content type
4. Updates `data/history.json` and pushes to GitHub
5. GitHub Pages serves the live dashboard

## Stack
- **Frontend:** Pure HTML/CSS/JS + Plotly.js
- **Pipeline:** Python + Playwright via OpenClaw browser
- **Hosting:** GitHub Pages
- **Automation:** OpenClaw cron

Built by Luka (OpenClaw AI agent) for Jigar @ Appforgelabs.
