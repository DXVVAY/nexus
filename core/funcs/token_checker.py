from core import *

valid_tokens = []

def check(token: str):
    threading.Thread(target=online, args=[token]).start()
    session = Client.get_session(token)
    result = session.get(f"https://discord.com/api/v9/users/@me/settings")
    if result.status_code == 200:
        log.success(f"{token[:35]}", "Valid")
        valid_tokens.append(token)
    elif "You need to verify your account in order to perform this action." in result.text:
        log.warning(f"{token[:35]}", "Locked")
    elif "Unauthorized" in result.text:
        log.failure(f"{token[:35]}", "Invalid")
    else:
        log.errors(token, result.text, result.status_code)

def token_checker():
    set_title(f"Token Checker")
    over_write = utility.ask("Overwrite Valid Tokens (y/n)")
    utility.run_threads(func=check, petc=False)
    if over_write == "y":
        with open(os.path.join('tokens.txt'), "w") as f:
            for token in valid_tokens:
                f.write(f"{token}\n")
        log.info("Wrote the valid tokens to tokens.txt")
    log.PETC()
