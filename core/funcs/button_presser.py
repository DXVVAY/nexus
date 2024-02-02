from core import *

def click(guild_id: str, channel_id: str, message_id: str, custom_id: str, application_id: str, token: str):
    threading.Thread(target=online, args=[token]).start()
    session = Client.get_session(token)
    session.headers.update({"referer": f"https://discord.com/channels/{guild_id}/{channel_id}"})
    result = session.post("https://discord.com/api/v9/interactions", json={
        "application_id": str(application_id),
        "channel_id": str(channel_id),
        "data": {"component_type": 2, "custom_id": str(custom_id)},
        "guild_id": str(guild_id),
        "message_flags": 0,
        "message_id": str(message_id),
        "nonce": utility.get_nonce(),
        'session_id': utility.rand_str(32),
        "type": 3,
    })
    log.success(f"{token[:50]}", "Pressed") if result.status_code == 204 else log.errors(token, result.text, result.status_code)

def button_presser():
    set_title(f"Button Presser")
    message = utility.message_info()
    guild_id = message["guild_id"]
    channel_id = message["channel_id"]
    message_id = message["message_id"]
    buttons = utility.get_buttons(
        token=utility.guild_token(guild_id, "Checker"),
        channel_id=channel_id,
        message_id=message_id
    )
    
    if buttons:
        print()
        for num, button in enumerate(buttons):
            label = button['label'].replace(' ', '') if button['label'] is not None else 'None'
            labels = f"    {PINK}[{MAGENTA}{num}{PINK}] {WHITE}{label}"
            print(labels)
        print()

        buttonnum = utility.ask("Button Number")
        for button in buttons:
            if buttons.index(button)==int(buttonnum):
                custom_id = button['custom_id']
                application_id = button['application_id']
                break

        thread = utility.ask("Thread Count")
        utility.run_threads(max_threads=thread, func=click, args=[guild_id, channel_id, message_id, custom_id, application_id])
    else:
        log.failure("Invalid message or message has no buttons")