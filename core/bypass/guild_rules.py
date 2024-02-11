from core import *

def bypass(log, guild_id: str, token: str):
    threading.Thread(target=online, args=[token]).start()
    session = Client.get_session(token)
    rules = session.get(f"https://discord.com/api/v9/guilds/{guild_id}/member-verification?with_guild=false").json()
    result = session.put(f"https://discord.com/api/v9/guilds/{guild_id}/requests/@me", json=rules)
    if result.status_code == 201:
        log.success(f"{token[:35]}", "Bypassed")
    elif result.status_code == 429:
        pass
    else:
        log.errors(token, result.text, result.status_code)

def bypass_rules(console, guild_id: str):
    set_title(f"Rules Bypass", console)
    log = logger(console)
    utility.run_threads(func=bypass, args=[log, guild_id], log=log)