from core import *

def friend(token: str, username: str, capkey: str, rqtoken: str):
    threading.Thread(target=online, args=[token]).start()
    while True:
        session = Client.get_session(token)
        capheads = lambda key, value: session.headers.update({key: value}) if key != "" else None
        capheads("x-captcha-key", capkey)
        capheads("x-captcha-rqtoken", rqtoken)
    
        result = session.post(f"https://discord.com/api/v9/users/@me/relationships", json={"session_id": utility.rand_str(32), "username": username})
        logcap = lambda message: log.success(f"{token[:35]}", message) if capkey == "" else log.success(f"With Captcha - {token[:35]}", message)
        usecap = lambda: (True, result.json()["captcha_rqtoken"], result.json()["captcha_rqdata"], result.json()["captcha_sitekey"]) if config.get("use_captcha") else (False, None, None, None)
    
        if result.status_code == 204:
            logcap("Frinded")
            return False, None, None, None
        elif result.text.startswith('{"captcha_key"'):
            log.failure(f"{token[:35]}", "Captcha")
            return usecap()
        else:
            log.errors(token, result.text, result.status_code)
            return False, None, None, None
    
def frineder(username: str, token: str):
    retry, rqtoken, rqdata, sitekey = friend(token, username, "","")
    if retry:
        capkey = Captcha(f"https://discord.com", sitekey=sitekey, rqdata=rqdata).solve()
        friend(token, username, capkey, rqtoken)

def user_mass_friend():
    set_title(f"Server Mass Friend")
    scraper(typ="usernames")
    thread = utility.ask("Thread Count")
    #if config.get("use_captcha") is True: Captcha.get_captcha_bal()
    while True:
        username = utility.get_random_user()
        utility.run_threads(max_threads=thread, func=frineder, args=[username], petc=False)