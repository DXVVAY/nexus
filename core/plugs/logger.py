from core import *

class logger:
    def __init__(self, prefix: str = "Nexus"):
        self.WHITE: str = "\u001b[37m"
        self.MAGENTA: str = "\033[38;5;97m"
        self.RED: str = "\033[38;5;196m"
        self.GREEN: str = "\033[38;5;40m"
        self.YELLOW: str = "\033[38;5;220m"
        self.BLUE: str = "\033[38;5;21m"
        self.PINK: str = "\033[38;5;176m"
        self.CYAN: str = "\033[96m"
        self.prefix: str = f"{self.PINK}[{self.MAGENTA}{prefix}{self.PINK}]"

    def get_time(self) -> str:
        return datetime.now().strftime("%H:%M:%S")
    
    def message(self, level: str, message: str) -> str:
        timer = json.loads(open('config.json', 'r').read()).get('log_timer', True)
        time_now = f"  {self.PINK}[{self.MAGENTA}{self.get_time()}{self.PINK}]  {self.WHITE}|" if timer else ""
        return f"  {self.prefix}  {self.WHITE}|{time_now}  {self.PINK}[{level}{self.PINK}]  {self.WHITE}->  {self.PINK}[{self.MAGENTA}{message}{self.PINK}]"

    def success(self, message: str, level: str = "Success"):
        print(self.message(f"{self.GREEN}{level}", f"{self.GREEN}{message}"))

    def warning(self, message: str, level: str = "Warning"):
        print(self.message(f"{self.YELLOW}{level}", f"{self.YELLOW}{message}"))

    def info(self, message: str, level: str = "Info"):
        print(self.message(f"{self.BLUE}{level}", f"{self.BLUE}{message}"))

    def failure(self, message: str, level: str = "Failure"):
        print(self.message(f"{self.RED}{level}", f"{self.RED}{message}"))

    def debug(self, message: str, level: str = "Debug"):
        print(self.message(f"{self.MAGENTA}{level}", f"{self.MAGENTA}{message}"))

    def scraper(self, message: str, level: str = "Scraper"):
        print(self.message(f"{self.BLUE}{level}", f"{self.BLUE}{message}"), end="\r", flush=True,)
    
    def captcha(self, message: str, level: str = "Captcha"):
        print(self.message(f"{self.CYAN}{level}", f"{self.CYAN}{message}"))

    def PETC(self):
        input(f"  {self.PINK}[{self.MAGENTA}Press Enter To Continue{self.PINK}]")

    def errors(self, token: str, res_text: str, res_status_code: int):
        errors: dict = {
            '{"captcha_key"': "Captcha",
            '{"message": "401: Unauthorized': "Unauthorized",
            "Cloudflare": "CloudFlare",
            "\"code\": 40007": "Banned",
            "\"code\": 20028": "Rate Limit",
            "retry_after": "Rate Limit",
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