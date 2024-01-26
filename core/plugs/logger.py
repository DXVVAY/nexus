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
        self.CYAN = "\033[96m"
        self.prefix = f"{self.PINK}[{self.MAGENTA}{prefix}{self.PINK}]"

    def get_time(self):
        return datetime.now().strftime("%H:%M:%S")
    
    def message(self, level: str, message: str):
        with open('config.json') as f:
            config = json.load(f)
        timer = config.get('log_timer')
        time_now = f" {self.PINK}[{self.MAGENTA}{self.get_time()}{self.PINK}] {self.WHITE}|" if timer else ""
        return f"  {self.prefix} {self.WHITE}|{time_now} {self.PINK}[{level}{self.PINK}] {self.WHITE}-> {self.PINK}[{self.MAGENTA}{message}{self.PINK}]"

    def success(self, message: str, level="Success"):
        print(self.message(f"{self.GREEN}{level}", f"{self.GREEN}{message}"))

    def warning(self, message: str, level="Warning"):
        print(self.message(f"{self.YELLOW}{level}", f"{self.YELLOW}{message}"))

    def info(self, message: str, level="Info"):
        print(self.message(f"{self.BLUE}{level}", f"{self.BLUE}{message}"))

    def failure(self, message: str, level="Failure"):
        print(self.message(f"{self.RED}{level}", f"{self.RED}{message}"))

    def debug(self, message: str, level="Debug"):
        print(self.message(f"{self.MAGENTA}{level}", f"{self.MAGENTA}{message}"))

    def scraper(self, message: str, level="Scraper"):
        print(self.message(f"{self.BLUE}{level}", f"{self.BLUE}{message}"), end="\r", flush=True,)
    
    def captcha(self, message: str, level="Captcha"):
        print(self.message(f"{self.CYAN}{level}", f"{self.CYAN}{message}"))

    def PETC(self):
        input(f"  {self.PINK}[{self.MAGENTA}Press Enter To Continue{self.PINK}]")

    def errors(self, token: str, res_text: str, res_status_code: int):
        errors = {
            '{"captcha_key"': "Captcha",
            '{"message": "401: Unauthorized': "Unauthorized",
            "Cloudflare": "CloudFlare",
            "\"code\": 40007": "Banned",
            "\"code\": 40002": "Locked",
            "\"code\": 10006": "Invalid Invite",
            "\"code\": 10004": "Not In Guild",
            "\"code\": 50013": "No Access",
            "\"code\": 50001": "No Access",
            "Unknown Message": "Unknown",
            "\"code\": 50033": "Invlid Recipient",
            "Cannot send messages to this user:": "Disabled DMS"
        }

        for er, msg in errors.items():
            if er in res_text:
                self.failure(f"{token[:50]}", msg)
                return

        self.failure(f"{token[:50]} - {res_text} {self.WHITE}- {self.RED}{res_status_code}")

log = logger()