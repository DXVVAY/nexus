from core import *

def send(token: str, message: str, channel_id: str, massping: str, amount=None):
    if massping == 'y':
        content = f"{message} - {utility.get_random_id(int(amount))} - {utility.rand_str(7)}"
    else:
        content = f"{message} - {utility.rand_str(7)}"
    session = Client.get_session(token, cookie=False)
    result = session.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", json={'session_id': utility.rand_str(32), "content": content})
    if result.status_code == 200:
        log.success(f"{token[:50]}", "Sent messagt")
    else:
        log.errors(token, result.text, result.status_code)

def token_spammer():
    set_title("Token Spammer")
    tokens = config.get_tokens()
    message = utility.ask("Message")
    channel_id = utility.ask("Channel ID")
    massping = utility.ask("Massping (y/n)")
    amount = 0
    
    if massping == 'y':
        guild_id = utility.ask("Guild ID")
        scraper(guild_id, channel_id, typ="ids")
        ids = utility.get_ids()
        amount = utility.ask(f"Amount Of pings (Don't exceed {len(ids)})")
    
    while True:
        if tokens:
            def thread_send(token):
                try:
                    token = utility.clean_token(token)
                    args = [token, message, channel_id, massping, amount]
                    send(*args)
                except Exception as e:
                    log.failure(e)

            threads = []
            for token in tokens:
                thread = threading.Thread(target=thread_send, args=(token,))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()
        else:
            return