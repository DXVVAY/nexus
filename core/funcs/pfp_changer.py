from core import *

def pfpchange(b64: str, token:str):
    threading.Thread(target=online, args=[token]).start()
    session = Client.get_session(token)
    result = session.patch(f"https://discord.com/api/v9/users/%40me/profile", json={"avatar": f"data:image/png;base64,{(b64.decode('utf-8'))}"})
    if result.status_code == 200:
        log.success(f"{token[:35]}", "Changed PFP")
    else:
        log.errors(token, result.text, result.status_code)

def pfp_changer():
    set_title("PFP Changer")
    Tk().withdraw()
    path = askopenfilename(filetypes=[("Image files", "*.png")])
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read())
    thread = utility.ask("Thread Count")
    utility.run_threads(max_threads=thread, func=pfpchange, args=[b64])