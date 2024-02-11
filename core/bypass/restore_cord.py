from core import *

def bypass(log, guild_id, bot_id, token):
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
            log.success(f"{token[:35]}", "Bypassed")
        else:
            log.errors(token, result.text, result.status_code)
    else:
        log.errors(token, result.text, result.status_code)

def restorecord_bypass(console, guild_id:str, bot_id:str):
    set_title(f"RestoreCord Bypass", console)
    log = logger(console)
    utility.run_threads(func=bypass, args=[log, guild_id, bot_id], log=log)