from .logger import *
from core import *

class Config:
    def __init__(self) -> None:
        self.file = os.path.join('config.json')
        self.tokens = os.path.join('tokens.txt')
        self.update_config()

    def update_config(self) -> None:
        self.content: Dict[str, Union[str, bool]] = {
            "nexus_key": "",
            "header_type": "Windows",
            "captcha_type": "Nexcha",
            "token_rpc": True,
            "log_timer": False,
            "use_captcha": True,
            "captcha_key": "",
            "chatgpt_key": "",
            }

        if not os.path.exists(self.file):
            with open(self.file, 'w') as f:
                json.dump(self.content, f, indent=3)
            log.info(f"Created Config File")
            sleep(2)

        if not os.path.exists(self.tokens):
            open('tokens.txt', 'w')
            log.info(f"Created tokens.txt File")
            sleep(2)

        if os.path.exists(self.file):
            existing_config = self.load('config.json')
            if all(key in existing_config for key in self.content.keys()):
                log.info(f"Config file is up to date")
                sleep(1)
            else:
                key = self.get("nexus_key")
                log.info("Config File Outdated!")
                log.info(f"Copy Your Nexus Key Before Updating -> {key}")
                log.PETC()
                with open(self.file, 'w') as f:
                    json.dump(self.content, f, indent=3)
                log.info(f"Config file has been updated to the latest and reset.")
                sleep(2)

    def load(self, f: str) -> Dict:
        try:
            with open(f, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError as e:
            print(e)
            raise

    def save(self, data: Dict) -> None:
        with open(self.file, 'w') as file:
            json.dump(data, file, indent=4)

    def _set(self, key: str, value: Union[str, bool]) -> None:
        data = self.load('config.json')
        data[key] = value
        self.save(data)

    def get(self, key: str, default: Optional[Union[str, bool]] = None) -> Union[str, bool, None]:
        data = self.load('config.json')
        return data.get(key, default) if default is not None else data.get(key)

    def remove(self, key: str) -> None:
        data = self.load('config.json')
        if key in data:
            del data[key]
            self.save(data)

    def get_tokens(self) -> List[str]:
        with open("tokens.txt", "r") as f:
            tokens = f.read().strip().splitlines()
        tokens = [token for token in tokens if token not in [" ", "", "\n"]]
        return tokens

    def get_random_token(self) -> Optional[str]:
        tokens = config.get_tokens()
        if tokens:
            return random.choice(tokens)
        else:
            return None

config = Config()