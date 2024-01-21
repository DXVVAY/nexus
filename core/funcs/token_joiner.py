from core import *

def join(invite, token):
    session = Client.get_session(token)
    result = session.post(f"https://discord.com/api/v9/invites/{invite}", json={"session_id": utility.rand_str(32)})
    if result.status_code == 200:
        log.success(f"{token[:50]}", "Joined")
    else:
        log.errors(token, result.text, result.status_code)

def token_joiner():
    set_title("Token Joiner")
    invite = utility.ask("Invite")
    invite = invite.split("/")[-1]
    thread = utility.ask("Thread Count")
    log.info(utility.get_server_name(invite), "Joining")
    utility.run_threads(max_threads=thread, func=join, args=[invite])