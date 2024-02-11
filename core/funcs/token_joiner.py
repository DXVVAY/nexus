from core import *

def join(token: str, invite: str, capkey: str, rqtoken: str):
    threading.Thread(target=online, args=[token]).start()
    session = Client.get_session(token)
    capheads = lambda key, value: session.headers.update({key: value}) if key != "" else None
    capheads("x-captcha-key", capkey)
    capheads("x-captcha-rqtoken", rqtoken)

    result = session.post(f"https://discord.com/api/v9/invites/{invite}", json={"session_id": utility.rand_str(32)})
    logcap = lambda message: log.success(f"{token[:50]}", message) if capkey == "" else log.success(f"With Captcha - {token[:50]}", message)
    usecap = lambda: (True, result.json()["captcha_rqtoken"], result.json()["captcha_rqdata"], result.json()["captcha_sitekey"]) if config.get("use_captcha") else (False, None, None, None)

    if result.status_code == 200:
        logcap("Joined")
        return False, None, None, None
    elif result.text.startswith('{"captcha_key"'):
        log.failure(f"{token[:50]}", "Captcha")
        return usecap()
    else:
        log.errors(token, result.text, result.status_code)
        return False, None, None, None

def joiner(invite: str, token: str):
    retry, rqtoken, rqdata, sitekey = join(token, invite, "", "")
    if retry:
        capkey = Captcha(f"https://discord.com", sitekey=sitekey, rqdata=rqdata).solve()
        join(invite, capkey, rqtoken, token)

def token_joiner():
    set_title("Token Joiner")
    invite = utility.ask("Invite")
    invite = invite.split("/")[-1]
    thread = utility.ask("Thread Count")
    log.info(utility.get_server_name(invite, Client.get_session()), "Joining")
    #if config.get("use_captcha") is True: Captcha.get_captcha_bal()
    utility.run_threads(max_threads=thread, func=joiner, args=[invite])