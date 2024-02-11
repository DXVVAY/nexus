from core import *

def react(emoji: str, message_id: str, channel_id: str, token: str):
    threading.Thread(target=online, args=[token]).start()
    session = Client.get_session(token)
    result = session.put(f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/%40me?location=Message&burst=false")
    if result.status_code == 204:
        log.success(f"{token[:35]}", "Reacted")
    else:
        log.errors(token, result.text, result.status_code)

def message_reactor():
    set_title(f"Message Reactor")
    message = utility.message_info()
    guild_id = message["guild_id"]
    channel_id = message["channel_id"]
    message_id = message["message_id"]

    emojis = utility.get_reactions(
        token=utility.guild_token(guild_id, "Checker"),
        channel_id=channel_id,
        message_id=message_id
    )

    
    if emojis:
        print()
        for num, emoji in enumerate(emojis):
            label = emoji['name'].replace(' ', '')
            labels = f"    {PINK}[{MAGENTA}{num}{PINK}] {WHITE}{label}"
            print(labels)
        print()

        emojinum = utility.ask("Emoji number")
        for emoji in emojis:
            if emojis.index(emoji) == int(emojinum):
                emoji = emoji['name'].replace(" ", "")
                break
            
        thread = utility.ask("Thread Count")
        utility.run_threads(max_threads=thread, func=react, args=[emoji.replace(":", "%3A"), message_id, channel_id])