from .logger import *
from .config import *
from .headers import *
from core import *

class Solvers: 
    def solve(self, solver_key, site_key : str, site_url : str) -> None:
        print(self.key)
    
    def get_balance(self):
        result = session.post("https://api.hcoptcha.online/api/getUserData", json={"api_key": solver_key})
        print(f"${result.json()['data']['balance']}")