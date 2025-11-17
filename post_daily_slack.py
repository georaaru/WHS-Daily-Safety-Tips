import os
from datetime import datetime, date
from zoneinfo import ZoneInfo  # Python 3.9+
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
# ---- CONFIG ----
TIMEZONE = "Europe/London"
SEND_AT_HOUR = 18     # 09:00 London local time
SEND_AT_MINUTE = 29
SKIP_WEEKENDS = False  # set True to skip Sat/Sun
# Env vars from GitHub Secrets
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")  # xoxb-...
CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID")      # C0123ABCD
# Your rotating messages
MESSAGES = [
    "Morning team — focus for today: clear blockers early, share wins often. :rocket:",
    "Remember: 1% better each day compounds wildly. What’s your 1% today?",
    "Safety > Speed. Smooth is fast. Let’s do it right the first time.",
    "Tiny kaizens beat giant maybes. Ship something small today.",
    "Be curious, be kind, be clear. That’s a great day recipe.",
    "Measure what matters, prune what doesn’t. Onward!",
    "Win the morning: one deep work block, one tough conversation, one tidy queue.",
    "Make it obvious. Make it easy. Make it done.",
    "Quality is a habit, not a hero moment.",
    "Less status, more substance. Ship!",
]
def london_now():
    return datetime.now(ZoneInfo(TIMEZONE))
def should_send_now():
    now = london_now()
    if SKIP_WEEKENDS and now.weekday() >= 5:  # 5=Sat, 6=Sun
        return False
    return now.hour == SEND_AT_HOUR and now.minute == SEND_AT_MINUTE
def pick_message_for_today():
    # Deterministic rotation: index = day count mod len(MESSAGES)
    # Using UTC date would drift against local time around midnight, so we use London local date.
    today = london_now().date()  # type: date
    days_since_anchor = (today - date(2020, 1, 1)).days
    idx = days_since_anchor % len(MESSAGES)
    return MESSAGES[idx]
def post_to_slack(text: str):
    if not SLACK_BOT_TOKEN or not CHANNEL_ID:
        raise SystemExit("Missing SLACK_BOT_TOKEN or SLACK_CHANNEL_ID.")
    client = WebClient(token=SLACK_BOT_TOKEN)
    try:
        client.chat_postMessage(channel=CHANNEL_ID, text=text)
    except SlackApiError as e:
        # surfacing the Slack error message helps debugging in Actions logs
        raise SystemExit(f"Slack error: {e.response.get('error')}")
def main():
    if not should_send_now():
        return
    post_to_slack(pick_message_for_today())
if __name__ == "__main__":
    main()
