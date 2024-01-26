from core import *

def send(message: str, channel_id: str, massping: str, amount: str, token: str):
    while True:
        try:
            content = (lambda x: f"{message} - {utility.get_random_id(int(amount))} - {utility.rand_str(7)}" if x == 'y' else f"{message} - {utility.rand_str(7)}")(massping)
            session = Client.get_session(token, cookie=False)
            result = session.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", json={'session_id': utility.rand_str(32), "content": content})
            if result.status_code == 200:
                log.success(f"{token[:50]}", "Sent message")
            else:
                log.errors(token, result.text, result.status_code)
        except Exception as e:
            log.failure(f"{str(e)[:70]}")

def token_spammer():
    set_title("Token Spammer")
    tokens = config.get_tokens()
    message = utility.ask("Message")
    channel_id = utility.ask("Channel ID")
    massping = utility.ask("Massping (y/n)")
    amount = "0"
    if massping == 'y':
        guild_id = utility.ask("Guild ID")
        scraper(guild_id, channel_id, typ="ids")
        ids = utility.get_ids()
        amount = utility.ask(f"Amount Of pings (Don't exceed {len(ids)})")

    thread = utility.ask("Thread Count")
    while True:
        utility.run_threads(max_threads=thread, func=send, args = [message, channel_id, massping, amount], petc=False)