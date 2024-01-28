from .hcopcha import *
from .nexcha import *

class Captcha:
    def __init__(self, url: str, sitekey: str, rqdata=""):
        self.url = url
        self.sitekey = sitekey
        self.rqdata = rqdata
        self.captcha_type = config._get('captcha_typ')
        self.types = {
            "Copcha": hcopcha,
            "Nexcha": nexcha
        }
        self.cap_type = self.types.get(self.captcha_type)

    def solve(self):
        if self.cap_type:
            cap = self.cap_type(url=self.url, sitekey=self.sitekey, rqdata=self.rqdata).solve()
            return cap

    @staticmethod
    def get_captcha_bal(self):
        if self.cap_type:
            self.cap_type.get_balance()