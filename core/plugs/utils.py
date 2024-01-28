from .logger import *
from .config import *
from .headers import *
from core import *

THIS_VERSION = "1.0.0"
whitelisted = ["1193273961476280451", "1188840335309291570", "1185267230380933170", "1174113517318705192"]

class utility:
    def rand_str(length: int) -> str:
        return ''.join(random.sample(string.ascii_lowercase+string.digits, length))
    
    def ask(text: str = ""):
        PINK = "\033[38;5;176m"
        MAGENTA = "\033[38;5;97m"
        ask = input(f"  {PINK}[{MAGENTA}{text}{PINK}]{MAGENTA} -> ")
        if ask in whitelisted:
            log.warning(f"Answer Whitelisted! Press enter to continue...")
            input()
            __import__("main").ui().main_screen()
        elif ask == "back":
            log.info(f"Going Back")
            sleep(2)
            __import__("main").ui().main_screen()
        return ask

    def message_info(link = None):
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

    def get_random_id(amount: int):
        users = utility.get_ids()
        randomid = random.sample(users, amount)
        return "<@" + "> <@".join(randomid) + ">"
    
    def get_ids():
        with open("scraped.txt", "r") as f:
            ids = f.read().strip().splitlines()
        ids = [idd for idd in ids if idd not in [" ", "", "\n"]]
        return ids
    
    def clear():
        system = os.name
        if system == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        return
    
    def make_menu(*options):
        PINK = "\033[38;5;176m"
        MAGENTA = "\033[38;5;97m"
        WHITE = "\u001b[37m"
        print()
        for num, option in enumerate(options, start=1):
            label = f"    {PINK}[{MAGENTA}{num}{PINK}] {WHITE}{option}"
            print(label)
        print()

    def clean_token(tokenn: str):
        r = re.compile(r"(.+):(.+):(.+)")
        if r.match(tokenn):
            return tokenn.split(":")[2]
        else:
            token = tokenn
        return token

    def get_client_type():
        heads = {
            "win": "Desktop", 
            "ios": "iOS"
        }
        typ = config.get("header_typ")
        return heads.get(typ, "Unknown")

    def get_server_name(invite, session):
        req = session.get(f"https://discord.com/api/v9/invites/{invite}?with_counts=true&with_expiration=true")
        if req.status_code == 200:
            res = req.json()
            name = res['guild']['name']
            return name
        else:
            return "Not Found"

    def guild_token(guild_id):
        tokens = config.get_tokens()
        for token in tokens:
            token = utility.clean_token(token)
            session = Client.get_session(token)
            r = session.get(f"https://discord.com/api/v9/guilds/{guild_id}")
            if r.status_code == 200:
                log.success(f"{token[:50]} Is in the guild", "Scraper")
                return token
            else:
                log.scraper(f"{token[:50]} Is not in guild")
        print()
        log.warning("No tokens in guild!", "Scraper")
        return None

    def run_threads(max_threads: str, func: types.FunctionType, args=[], petc=True):
        max_threads = int(max_threads)
        tokens = config.get_tokens()

        if tokens:
            with ThreadPoolExecutor(max_workers=max_threads) as executor:
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
                if petc:
                    log.PETC()
        else:
            log.warning("No tokens were found in tokens.txt")
            log.PETC()