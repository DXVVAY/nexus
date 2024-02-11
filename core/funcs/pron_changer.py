from core import *

def pchanger(pronouns: str, token: str):
    threading.Thread(target=online, args=[token]).start()
    session = Client.get_session(token)
    result = session.patch(f"https://discord.com/api/v9/users/%40me/profile", json={"pronouns": pronouns})
    if result.status_code == 200:
        log.success(f"{token[:35]}", "Changed pronouns")
    else:
        log.errors(token, result.text, result.status_code)

def pron_changer():
    set_title("Pronouns Changer")
    pronouns = utility.ask("Pronouns")
    thread = utility.ask("Thread Count")
    utility.run_threads(max_threads=thread, func=pchanger, args=[pronouns])