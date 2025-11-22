import os
from datetime import date
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Env vars from GitHub Secrets
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")  # xoxb-...
CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID")      # C0123ABCD

# Rotating WHS tips
MESSAGES = [
    "*:safetogo:Safe to Go Tip:* Use your powerzone: Keeping items in your powerzone — the area from mid-thigh to mid-chest — helps you stay safe when lifting, lowering, and turning.",
   
    "*:safetogo:Safe to Go Tip:* The right equipment for the job: Using correct personal protective equipment (PPE) :gloves: , like gloves for proper grasping, reduces the risk of musculoskeletal disorders (MSDs) such as sprains and strains.",
   
    "*:safetogo:Safe to Go Tip:* Switch sides: Alternating between your left and right sides helps your body maintain balance and reduces strain.",
   
    "*:safetogo:Safe to Go Tip:* Practise the team lift: Test the weight before lifting and use both hands. Ask for help if an item is too heavy or awkward.",
   
    "*:safetogo:Safe to Go Tip:* Stretch it out: Stretch before and after work to reduce fatigue and improve range of motion.",
   
    "*:safetogo:Safe to Go Tip:* Select the right tool: Use the correct equipment in the proper way to reduce effort and avoid unnecessary strain.",
   
    "*:safetogo:Safe to Go Tip:* Reduce exposure to MSD risk factors: Test the weight of items before lifting, keep them close to your body, and take micro-breaks to stretch while working.",
]

def pick_message_for_today() -> str:
    """Deterministic rotation: based on date, no state file needed."""
    today = date.today()
    days_since_anchor = (today - date(2020, 1, 1)).days
    idx = days_since_anchor % len(MESSAGES)
    return MESSAGES[idx]

def post_to_slack(text: str) -> None:
    if not SLACK_BOT_TOKEN or not CHANNEL_ID:
        raise SystemExit("Missing SLACK_BOT_TOKEN or SLACK_CHANNEL_ID.")
    client = WebClient(token=SLACK_BOT_TOKEN)
    try:
        client.chat_postMessage(channel=CHANNEL_ID, text=text)
    except SlackApiError as e:
        raise SystemExit(f"Slack error: {e.response.get('error')}")

def main() -> None:
    # Always send exactly one message whenever GitHub runs this script
    post_to_slack(pick_message_for_today())

if __name__ == "__main__":
    main()
