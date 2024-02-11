from core import *

valid_tokens = []

def check(guild_id: str, token: str):
    threading.Thread(target=online, args=[token]).start()
    session = Client.get_session(token)
    result = session.get(f"https://discord.com/api/v9/guilds/{guild_id}")
    if result.status_code == 200:
        log.success(f"{token[:50]}", "In Guild")
        valid_tokens.append(token)
    else:
        log.errors(token, result.text, result.status_code)

def server_checker():
    set_title(f"Token Server Checker")
    guild_id = utility.ask("Guild ID")
    thread = utility.ask("Thread Count")
    utility.run_threads(max_threads=thread, func=check, args=[guild_id], petc=False)
    with open(os.path.join('tokens.txt'), "w") as f:
        for token in valid_tokens:
            f.write(f"{token}\n")
    log.info("Wrote the tokens in the guild to tokens.txt")
    log.PETC()
