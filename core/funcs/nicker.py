from core import *

def nchanger(Nickname: str, token: str):
    threading.Thread(target=online, args=[token]).start()
    session = Client.get_session(token)
    result = session.patch(f"https://discord.com/api/v9/users/@me", json={"global_name": Nickname})
    if result.status_code == 200:
        log.success(f"{token[:35]}", "Changed Global Nickname")
    else:
        log.errors(token, result.text, result.status_code)

def Nick_changer():
    set_title("Nick Changer")
    Nickname = utility.ask("Nick:")
    thread = utility.ask("Thread Count")
    utility.run_threads(max_threads=thread, func=nchanger, args=[Nickname])