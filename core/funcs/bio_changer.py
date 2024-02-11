from core import *

def bchanger(bio: str, token: str):
    threading.Thread(target=online, args=[token]).start()
    session = Client.get_session(token)
    result = session.patch(f"https://discord.com/api/v9/users/%40me/profile", json={"bio": bio})
    if result.status_code == 200:
        log.success(f"{token[:50]}", "Changed bio")
    else:
        log.errors(token, result.text, result.status_code)

def bio_changer():
    set_title("Bio Changer")
    bio = utility.ask("Bio")
    thread = utility.ask("Thread Count")
    utility.run_threads(max_threads=thread, func=bchanger, args=[bio])