import requests
from langchain_core.tools import tool
from agentforge.backend.core.config import settings

@tool
def slack_send_message(channel: str, text: str, thread_ts: str = None) -> str:
    """
    Sends a message to a Slack channel.
    Args:
        channel: The channel ID or name.
        text: The message content (markdown supported).
        thread_ts: Optional timestamp of a thread to reply to.
    """
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {settings.SLACK_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel": channel,
        "text": text
    }
    if thread_ts:
        payload["thread_ts"] = thread_ts
        
    try:
        response = requests.post(url, headers=headers, json=payload)
        res_data = response.json()
        if res_data.get("ok"):
            return "Message sent to Slack."
        return f"Slack API error: {res_data.get('error')}"
    except Exception as e:
        return f"Failed to send Slack message: {str(e)}"
