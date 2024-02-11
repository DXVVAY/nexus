from core import*

def get_sub_id(token: str):
    session = Client.get_session(token)
    result = session.get( "https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots")
    sub_ids = []
    if result.status_code == 200:
        data = result.json()
        for sub in data:
            sub_ids.append(sub["id"])
        if sub_ids is None or len(sub_ids) == 0:
            log.failure("Token Has No Boosts")
            return None
        return sub_ids

def boost(guild_id: str, token: str):
    threading.Thread(target=online, args=[token]).start()
    session = Client.get_session(token)
    sub_ids = get_sub_id(token)
    for i in range(len(sub_ids)):
        result = session.put(f"https://discord.com/api/v9/guilds/{guild_id}/premium/subscriptions", json={"user_premium_guild_subscription_slot_ids": [f"{sub_ids[i]}"]})
        if result.status_code == 201:
            log.success(f"{token[:35]}", "Boosted")
        else:
            log.errors(token, result.text, result.status_code)

def server_booster():
    set_title("Server Booster")
    guild_id = utility.ask("Guild ID", True)
    thread = utility.ask("Thread Count")
    utility.run_threads(max_threads=thread, func=boost, args=[guild_id])