from .logger import *
from core import *

class Config:
    def __init__(self):
        self.file = os.path.join('config.json')
        self.tokens = os.path.join('tokens.txt')
        self.update_config()

    def update_config(self):
        self.content = {
            "nexus_key": "",
            "header_typ": "",
            "log_timer": False,
            "use_captcha": True,
            "captcha_typ": "Custom",
            "captcha_key": "",
            "chatgpt_key": "",
            "debug_mode": False
            }

        config_exists = os.path.exists(self.file)
        tokens_exists = os.path.exists(self.tokens)

        if not config_exists:
            with open(self.file, 'w') as f:
                json.dump(self.content, f, indent=3)
            log.info(f"Created Config File")
            sleep(2)

        if not tokens_exists:
            with open('tokens.txt', 'w') as f:
                f.write('')
            log.info(f"Created tokens.txt File")
            sleep(2)

        if config_exists:
            existing_config = self.load('config.json')
            if all(key in existing_config for key in self.content.keys()):
                log.info(f"Config file is up to date")
                sleep(1)
            else:
                key = self.get("xvirus_key")
                log.info(f"Config File Outdated Please Copy Your Nexus Key Before Updating -> {key}")
                log.PETC()
                with open(self.file, 'w') as f:
                    json.dump(self.content, f, indent=3)
                log.info(f"Config file has been updated to the latest and reset.")
                sleep(2)

    def load(self, f):
        path = os.path.join(f)
        try:
            with open(path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError as e:
            print(e)
            return {}

    def save(self, data):
        with open(self.file, 'w') as file:
            json.dump(data, file, indent=4)

    def _set(self, key, value):
        data = self.load('config.json')
        data[key] = value
        self.save(data)

    def get(self, key, default=None):
        data = self.load('config.json')
        return data.get(key, default) if default is not None else data.get(key)

    def remove(self, key):
        data = self.load('config.json')
        if key in data:
            del data[key]
            self.save(data)

    def get_tokens(self):
        with open("tokens.txt", "r") as f:
            tokens = f.read().strip().splitlines()
        tokens = [token for token in tokens if token not in [" ", "", "\n"]]
        return tokens

    def get_random_token(self):
        tokens = config.get_tokens()
        if tokens:
            return random.choice(tokens)
        else:
            return None

config = Config()