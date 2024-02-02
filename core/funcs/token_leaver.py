from core import *

def leave(guild_id: str, token: str):
    threading.Thread(target=online, args=[token]).start()
    session = Client.get_session(token)
    result = session.delete(f"https://discord.com/api/v9/users/@me/guilds/{guild_id}", json={"session_id": utility.rand_str(32)})
    if result.status_code == 204:
        log.success(f"{token[:50]}", "Left")
    else:
        log.errors(token, result.text, result.status_code)

def token_leaver():
    set_title("Token Leaver")
    guild_id = utility.ask("Guild ID")
    thread = utility.ask("Thread Count")
    utility.run_threads(max_threads=thread, func=leave, args=[guild_id])