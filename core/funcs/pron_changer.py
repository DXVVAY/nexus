from core import *

def pchanger(pronouns: str, token: str):
    session = Client.get_session(token)
    result = session.patch(f"https://discord.com/api/v9/users/%40me/profile", json={"pronouns": pronouns})
    if result.status_code == 200:
        log.success(f"{token[:50]}", "Changed pronouns")
    else:
        log.errors(token, result.text, result.status_code)

def pron_changer():
    set_title("Pronoun Changer")
    pronouns = utility.ask("Pronouns")
    thread = utility.ask("Thread Count")
    utility.run_threads(max_threads=thread, func=pchanger, args=[pronouns])