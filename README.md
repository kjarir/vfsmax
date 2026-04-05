# VFSMAX — Intelligent VFS Monitoring & Booking

VFSMAX is the most resilient and AI-powered VFS Global appointment monitoring and booking system.

## 🚀 Features
- **Stealth Browser**: Playwright with fingerprint randomization and proxy rotation.
- **AI Decision Engine**: GPT-4o for CAPTCHA solving and slot scoring.
- **Failure Intelligence**: Automatic recovery from IP bans and website changes.
- **Multi-Channel Alerts**: Telegram, WhatsApp, Email, Slack, Discord.
- **Real-time Dashboard**: Beautiful React-based control panel.
- **Slot Prediction**: ML model predicting when slots are likely to appear.

## 📁 Repository Structure
- `/backend`: FastAPI, Celery, Playwright Engine, ML models.
- `/frontend`: React dashboard with Recharts and Tailwind.
- `/infrastructure`: Docker, Prometheus, Grafana.
- `/cli`: Python Typer app for system management.

## 🛠️ Quick Start
1. Clone the repository.
2. `cp .env.example .env` and fill in your API keys.
3. Run with one command:
   ```bash
   docker compose up --build
   ```

## 🧠 Stealth Philosophy
- **Bezier Mouse Movements**: Mimics human jitter and speed variance.
- **Variable Typing Speed**: Types at 40-120 WPM with random errors.
- **Proxy Rotation**: Geographical matching proxy pool.
- **Fingerprint Profile Database**: 500+ scraped real-device profiles.

## 🛠️ Requirements
- Docker & Docker Compose
- Python 3.11+ (Local development)
- Node.js 18+ (Local development)
- Open AI API Key (for GPT-4o Vision)

---
*Built for resilience and peace of mind by Antigravity AI.*
