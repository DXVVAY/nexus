from core import *

def tspammer(channel_id, message, token):
    session = Client.get_session(token)
    result = session.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", json={"content": message, "flags": 0, "mobile_network_type": "unknown", "tts": False})
    if result.status_code == 204:
        log.success(f"{token[:50]}", "Sent messagt")
    else:
        log.errors(token, result.text, result.status_code)

def token_spammer():
    set_title("Token Spammer")
    message = utility.ask("Message")
    channel_id = utility.ask("Channel ID")
    thread = utility.ask("Thread Count")
    utility.run_threads(max_threads=thread, func=tspammer, args=[channel_id, message])