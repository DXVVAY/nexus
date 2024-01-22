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
            return 
        elif ask == "back":
            log.info(f"Going Back")
            sleep(2)
            return
        return ask
    
    def get_random_id(amount: int):
        f_path = os.path.join(os.getenv('LOCALAPPDATA'), 'xvirus_config')
        file = os.path.join(f_path, 'xvirus_ids')
        with open(file, "r", encoding="utf8") as f:
            users = [line.strip() for line in f.readlines()]
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

    def get_server_name(invite):
        req = requests.get(f"https://discord.com/api/v9/invites/{invite}?with_counts=true&with_expiration=true")
        if req.status_code == 200:
            res = req.json()
            name = res['guild']['name']
            return name
        else:
            return "Not Found"

    def run_threads(max_threads: str, func: types.FunctionType, args=[]):
        max_threads = int(max_threads)
        tokens = config.get_tokens()

        threads = []

        if tokens:
            for token in tokens:
                try:
                    token = utility.clean_token(token)
                    args.append(token)
                    try:
                        thread = threading.Thread(target=func, args=args)
                        thread.start()
                        threads.append(thread)
                    except Exception as e:
                        log.failure(f"{e[:70]}")
                    args.remove(token)
                except Exception as e:
                    log.failure(f"{e[:70]}")

            for thread in threads:
                try:
                    thread.join()
                except tls_client.exceptions.TLSClientExeption as e:
                    log.failure(f"{e[:70]}")
                except Exception as e:
                    log.failure(f"{e[:70]}")

            log.PETC()
        else:
            log.warning("No tokens were found in tokens.txt")
            log.PETC()