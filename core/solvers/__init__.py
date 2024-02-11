from .hcopcha import *
from .nexcha import *
from .capsolver import *
from core import *

class Captcha:
    def __init__(self, url: str, sitekey: str, rqdata: str = ""):
        self.url: str = url
        self.sitekey: str = sitekey
        self.rqdata: str = rqdata
        self.type: str = config.get('captcha_type')
        self.types: dict = {
            "Hcopcha": hcopcha,
            "Nexcha": nexcha,
            "Capsolver": capsolver
        }
        self.cap_type = self.types.get(self.type)

    def solve(self) -> str:
        if self.cap_type:
            cap = self.cap_type().solve(url=self.url, sitekey=self.sitekey, rqdata=self.rqdata)
            return cap

    def get_captcha_bal(self) -> None:
        if self.cap_type:
            self.cap_type.get_balance()
