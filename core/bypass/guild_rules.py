from core import *

def bypass(guild_id: str, token: str):
    threading.Thread(target=online, args=[token]).start()
    session = Client.get_session(token)
    rules = session.get(f"https://discord.com/api/v9/guilds/{guild_id}/member-verification?with_guild=false").json()
    result = session.put(f"https://discord.com/api/v9/guilds/{guild_id}/requests/@me", json=rules)
    if result.status_code == 201:
        log.success(f"{token[:50]}", "Bypassed")
    elif result.status_code == 429:
        pass
    else:
        log.errors(token, result.text, result.status_code)

def bypass_rules():
    set_title(f"Rules Bypass")
    guild_id = utility.ask("Guild ID")
    thread = utility.asknum("Thread Count")
    utility.run_threads(max_threads=thread, func=bypass, args=[guild_id])