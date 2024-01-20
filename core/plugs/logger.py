from core import *

class logger:
    def __init__(self, prefix="Nexus"):
        self.WHITE = "\u001b[37m"
        self.MAGENTA = "\033[38;5;97m"
        self.RED = "\033[38;5;196m"
        self.GREEN = "\033[38;5;40m"
        self.YELLOW = "\033[38;5;220m"
        self.BLUE = "\033[38;5;21m"
        self.PINK = "\033[38;5;176m"
        self.prefix = f"{self.PINK}[{self.MAGENTA}{prefix}{self.PINK}]"

    def get_time(self):
        return datetime.now().strftime("%H:%M:%S")
    
    def message(self, level, message):
        with open('config.json') as f:
            config = json.load(f)
        timer = config.get('log_timer')
        time_now = f" {self.PINK}[{self.MAGENTA}{self.get_time()}{self.PINK}] {self.WHITE}|" if timer else ""
        return f"{self.prefix} {self.WHITE}|{time_now} {self.PINK}[{level}{self.PINK}] {self.WHITE}-> {self.PINK}[{self.MAGENTA}{message}{self.PINK}]"

    def success(self, message, level="Success"):
        print(self.message(f"{self.GREEN}{level}", f"{self.GREEN}{message}"))

    def warning(self, message, level="Warning"):
        print(self.message(f"{self.YELLOW}{level}", f"{self.YELLOW}{message}"))

    def info(self, message, level="Info"):
        print(self.message(f"{self.BLUE}{level}", f"{self.BLUE}{message}"))

    def failure(self, message, level="Failure"):
        print(self.message(f"{self.RED}{level}", f"{self.RED}{message}"))

    def debug(self, message, level="Debug"):
        print(self.message(f"{self.MAGENTA}{level}", f"{self.MAGENTA}{message}"))

    def scraper(self, message, level="Scraper"):
        print(self.message(f"{self.BLUE}{level}", f"{self.BLUE}{message}"), end="\r", flush=True,)
    
    def PETC(self):
        input(f"{self.PINK}[{self.MAGENTA}Press Enter To Continue{self.PINK}]")

log = logger()