from .logger import *
from .config import *
from .headers import *
from core import *

THIS_VERSION: str = "1.0.0"
whitelisted: List[str] = ["1193273961476280451", "1188840335309291570", "1185267230380933170", "1174113517318705192", "1194007607959105607"]
PINK: str = "\033[38;5;176m"
MAGENTA: str = "\033[38;5;97m"
WHITE: str = "\u001b[37m"

class utility:
    def rand_str(length: int) -> str:
        return ''.join(random.sample(string.ascii_lowercase+string.digits, length))
    
    def ask(text: str = "", white: bool = False) -> str:
        ask: str = input(f"  {PINK}[{MAGENTA}{text}{PINK}]{MAGENTA} -> ")
        if not white and any(w in ask for w in whitelisted):
            log.warning(f"Answer Whitelisted! Press enter to continue...")
            input()
            __import__("main").ui().main_screen()
        elif ask == "back":
            log.info(f"Going Back")
            sleep(2)
            __import__("main").ui().main_screen()
        return ask

    def message_info(link = None) -> Optional[Dict[str, str]]:
        if link is None:
            link = utility.ask("Message link")
        pattern = re.compile(r"^https:\/\/(ptb\.|canary\.)?discord\.com\/channels\/\d+\/\d+\/\d+$")
        if pattern.match(link):
            parts = link.split("/")
            guild_id, channel_id, message_id = parts[4], parts[5], parts[6]
            return {
                "guild_id": guild_id,
                "channel_id": channel_id,
                "message_id": message_id
            }
        else:
            log.warning("Invalid message link")
            return None

    def get_random_id(amount: int) -> Optional[str]:
        users = utility.get_ids()
        try:
            randomid = random.sample(users, amount)
            return "<@" + "> <@".join(randomid) + ">"
        except Exception as e:
            log.errors(e)
        return None
    
    def get_ids() -> List[str]:
        with open("scraped.txt", "r", encoding="utf-8") as f:
            ids = f.read().strip().splitlines()
        ids = [idd for idd in ids if idd not in [" ", "", "\n"]]
        return ids
    
    def get_random_user() -> Optional[str]:
        users = utility.get_ids()
        try:
            rand = random.choice(users)
            return rand
        except Exception as e:
            log.errors(e)
        return None
    
    def get_users() -> List[str]:
        with open("scraped.txt", "r") as f:
            users = f.read().strip().splitlines()
        users = [user for user in users if user not in [" ", "", "\n"]]
        return users
    
    def clear() -> None:
        system = os.name
        if system == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        return
    
    def make_menu(*options: str) -> None:
        print()
        for num, option in enumerate(options, start=1):
            label = f"    {PINK}[{MAGENTA}{num}{PINK}] {WHITE}{option}"
            print(label)
        print()

    def clean_token(token: str) -> str:
        if re.match(r"(.+):(.+):(.+)", token):
            return token.split(":")[2]
        return token

    def get_client_type() -> str:
        heads: Dict[str, str] = {
            "Windows": "Desktop", 
            "iOS": "iOS"
        }
        typ = config.get("header_type")
        return heads.get(typ, "Unknown")

    def get_server_name(invite: str, session) -> str:
        req = session.get(f"https://discord.com/api/v9/invites/{invite}?with_counts=true&with_expiration=true")
        if req.status_code == 200:
            res = req.json()
            name = res['guild']['name']
            return name
        else:
            return "Not Found"

    def guild_token(guild_id: str, typ: str = "Scraper") -> Optional[str]:
        tokens = config.get_tokens()
        for token in tokens:
            token = utility.clean_token(token)
            session = Client.get_session(token)
            r = session.get(f"https://discord.com/api/v9/guilds/{guild_id}")
            if r.status_code == 200:
                log.success(f"{token[:35]} Is in the guild", typ)
                return token
            else:
                log.scraper(f"{token[:35]} Is not in guild", typ)
        print()
        log.warning("No tokens in guild!", typ)
        return None

    def get_buttons(token: str, channel_id: str, message_id: str) -> Optional[List[Dict[str, Union[str, bool]]]]:
        try:
            session = Client.get_session(token)
            response = session.get(f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=1&around={message_id}").json()
            message = response[0]
            buttons = []
            for component in message["components"]:
                for button in component.get("components", []):
                    buttons.append({
                        "label": button.get("label"),
                        "custom_id": button["custom_id"],
                        "application_id": message["author"]["id"],
                    })

            return buttons
        except Exception as e:
            log.failure(e)
            return None

    def get_reactions(token: str, channel_id: str, message_id: str) -> Optional[List[Dict[str, Union[str, int, bool]]]]:
        try:
            session = Client.get_session(token)
            response = session.get(f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=1&around={message_id}").json()
            reactions = response[0].get("reactions", [])

            if not reactions:
                return None

            return [{
                "name": f"{r['emoji']['name']}" if r['emoji']['id'] is None else f"{r['emoji']['name']}:{r['emoji']['id']}",
                "count": r["count"],
                "custom": r['emoji']['id'] is not None
            } for r in reactions]
        except Exception as e:
            log.failure(e)
            return None

    def get_nonce() -> str:
        return str(round(Decimal(time.time()*1000-1420070400000)*4194304))

    def rand_time() -> int:
        return (int(delorean.Delorean(datetime.now(timezone.utc), timezone="UTC").epoch) * 1000) - random.randint(100000, 10000000)
    
    def randp(data):
        return next(iter(random.choices(
            population = list({k: v / sum(data.values()) for k, v in data.items()}),
            weights = {k: v / sum(data.values()) for k, v in data.items()}.values(),
            k = 1
        )))
    
    def run_threads(func: types.FunctionType, args=[], petc: bool = True, log=log) -> None:
        tokens = config.get_tokens()

        if tokens:
            with ThreadPoolExecutor(max_workers=int("17")) as executor:
                futures = []
                for token in tokens:
                    try:
                        token = utility.clean_token(token)
                        args.append(token)
                        try:
                            future = executor.submit(func, *args)
                            futures.append(future)
                        except Exception as e:
                            log.failure(f"{str(e)[:70]}")
                        args.remove(token)
                    except Exception as e:
                        log.failure(f"{str(e)[:70]}")

                for future in futures:
                    try:
                        future.result()
                    except tls_client.exceptions.TLSClientExeption as e:
                        log.failure(f"{str(e)[:70]}")
                    except Exception as e:
                        log.failure(f"{str(e)[:70]}")
        else:
            log.warning("No tokens were found in tokens.txt")
