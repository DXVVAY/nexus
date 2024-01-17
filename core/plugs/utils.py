from .logger import *
from .config import *
from .headers import *
from core import *

THIS_VERSION = "1.0.0"
whitelisted = ["1193273961476280451", "1188840335309291570", "1185267230380933170", "1174113517318705192"]

class utility:
    def rand_str(length:int) -> str:
        return ''.join(random.sample(string.ascii_lowercase+string.digits, length))
    
    def ask(text: str = ""):
        PINK = "\033[38;5;176m"
        MAGENTA = "\033[38;5;97m"
        ask = input(f"{PINK}[{MAGENTA}{text}{PINK}]{MAGENTA} -> ")
        if ask in whitelisted:
            log.warning(f"Answer Whitelisted! Press enter to continue...")
            input()
            return 
        elif ask == "back":
            log.info(f"Going Back")
            sleep(2)
            return
        return ask
    
    def get_random_id(id):
        f_path = os.path.join(os.getenv('LOCALAPPDATA'), 'xvirus_config')
        file = os.path.join(f_path, 'xvirus_ids')
        with open(file, "r", encoding="utf8") as f:
            users = [line.strip() for line in f.readlines()]
        randomid = random.sample(users, id)
        return "<@" + "> <@".join(randomid) + ">"
    
    def get_ids():
        with open("scraped_ids.txt", "r") as f:
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

    def clean_token(tokenn):
        r = re.compile(r"(.+):(.+):(.+)")
        if r.match(tokenn):
            return tokenn.split(":")[2]
        else:
            token = tokenn
        return token

    def run_threads(max_threads, func, args=[], delay=0):
        def thread_complete(future):
            debug = config.get("debug_mode")
            try:
                result = future.result()
            except Exception as e:
                if debug:
                    if "failed to do request" in str(e):
                        log.debug(f"Proxy Error -> {str(e)[:80]}...")
                    else:
                        log.debug(f"Error -> {e}")
                else:
                    pass

        def stop_threads(signum, frame):
            nonlocal stop_flag
            stop_flag = True

        max_threads = int(max_threads)
        stop_flag = False
        signal.signal(signal.SIGINT, stop_threads)
        tokens = config.get_tokens()

        if tokens:
            with ThreadPoolExecutor(max_workers=max_threads) as executor:
                for token in tokens:
                    try:
                        token = utility.clean_token(token)
                        args.append(token)
                        future = executor.submit(func, *args)
                        future.add_done_callback(thread_complete)
                        args.remove(token)
                        time.sleep(delay)
                    except Exception as e:
                        log.failure(e)

                    if stop_flag:
                        break

            log.PETC()
        else:
            log.warning("No tokens were found in tokens.txt")
            log.PETC()