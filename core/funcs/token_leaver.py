from core import *

def leave(log, guild_id: str, token: str):
    threading.Thread(target=online, args=[token]).start()
    session = Client.get_session(token)
    result = session.delete(f"https://discord.com/api/v9/users/@me/guilds/{guild_id}", json={"session_id": utility.rand_str(32)})
    if result.status_code == 204:
        log.success(f"{token[:35]}", "Left")
    else:
        log.errors(token, result.text, result.status_code)

def token_leaver(console, guild_id):
    set_title("Token Leaver", console)
    log = logger(console)
    utility.run_threads(func=leave, args=[log, guild_id])