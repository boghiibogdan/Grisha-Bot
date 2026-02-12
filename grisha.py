import os
import sys
import requests
from datetime import datetime, timezone

# ==============================
# Environment Variables (Secrets)
# ==============================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "").strip()

CITY = "London"
COUNTRY = "GB"
UNITS = "metric"  # metric = Celsius

RUN_MODE = os.getenv("RUN_MODE", "daily").strip().lower()
BRAND_NAME = "Rozashi"


# ==============================
# Safety Check
# ==============================
def require_env():
    missing = []
    if not TELEGRAM_BOT_TOKEN:
        missing.append("TELEGRAM_BOT_TOKEN")
    if not TELEGRAM_CHAT_ID:
        missing.append("TELEGRAM_CHAT_ID")
    if not OPENWEATHER_API_KEY:
        missing.append("OPENWEATHER_API_KEY")
    if missing:
        print(f"Missing required env vars: {', '.join(missing)}")
        sys.exit(1)


# ==============================
# Weather (First Line Always)
# ==============================
def get_weather_line():
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": f"{CITY},{COUNTRY}",
            "appid": OPENWEATHER_API_KEY,
            "units": UNITS,
        }
        r = requests.get(url, params=params, timeout=20)
        data = r.json()

        desc = data["weather"][0]["description"].capitalize()
        temp = round(data["main"]["temp"])

        return f"{CITY}: {desc}, {temp}°C"

    except Exception:
        return f"{CITY}: Weather unavailable"


# ==============================
# Telegram Send
# ==============================
def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
    }

    r = requests.post(url, data=payload)

    if r.status_code != 200:
        print("Telegram error:", r.text)
        sys.exit(1)


# ==============================
# Daily Brief
# ==============================
def daily_brief():
    weather = get_weather_line()

    msg = f"""
{weather}

<b>Grisha — {BRAND_NAME} Daily Brief</b>

#1 Priority:
Finish the Shopify store conversion basics (homepage + product page + trust).

3 Tasks (1–2h total):
• Improve homepage clarity + CTA + luxury feel
• Fix product page (size guide, delivery, returns)
• Add trust signals (FAQ, shipping, contact)

Marketing Action:
Create 1 AI influencer post (clean, minimal, luxury look).

Discipline:
No perfection today. Ship progress. 1 hour minimum.

Strategy Insight:
Luxury brands win through consistency and restraint, not volume.

Reply with:
DONE / BLOCKED / NEED DECISION
"""

    return msg


# ==============================
# Weekly Review
# ==============================
def weekly_review():
    weather = get_weather_line()

    msg = f"""
{weather}

<b>Grisha — {BRAND_NAME} Weekly Strategy Review</b>

Score yourself honestly:
• Store readiness (0–10)
• Content posted (#)
• Consistency (#/7)
• Launch readiness (0–10)

Focus for next week:
Finish store + publish first 3–5 clean luxury posts.

Rule:
1 hour daily minimum. Consistency > intensity.

Reply with your scores and Grisha will identify your main bottleneck.
"""

    return msg


# ==============================
# Main
# ==============================
def main():
    require_env()

    if RUN_MODE == "weekly":
        text = weekly_review()
    else:
        text = daily_brief()

    send_telegram(text)
    print("Message sent successfully.")


if __name__ == "__main__":
    main()
