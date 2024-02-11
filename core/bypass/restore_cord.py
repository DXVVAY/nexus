from core import *

def bypass(guild_id: str, bot_id: str, token: str):
    threading.Thread(target=online, args=[token]).start()
    session = Client.get_session(token)
    params = {
        "client_id":{bot_id},
        "response_type":"code",
        "redirect_uri": "https://restorecord.com/api/callback",
        "scope":"identify guilds.join",
        "state":{guild_id}
    }
    auth = session.post(f"https://discord.com/api/v9/oauth2/authorize", params=params, json={"permissions":"0","authorize":True})
    if "location" in auth.text:
        result = session.get(auth.json()["location"], allow_redirects=True)
        if result.status_code in [307, 403, 200]:
            log.success(f"{token[:50]}", "Bypassed")
        else:
            log.errors(token, result.text, result.status_code)
    else:
        log.errors(token, result.text, result.status_code)

def restorecord_bypass():
    set_title(f"RestoreCord Bypass")
    guild_id = utility.ask("Guild ID")
    bot_id = utility.ask("Bot ID")
    thread = utility.ask("Thread Count")
    utility.run_threads(max_threads=thread, func=bypass, args=[guild_id, bot_id])