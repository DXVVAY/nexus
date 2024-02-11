from core import *

class nexcha:
    def __init__(self):
        self.api_key: str = "DEXV-rhdgva-82tk4q-g8nlj6-rpgmw0"
        self.s: Optional[float] = None

    def solve(self, url: str, sitekey: str, rqdata: str = "") -> Optional[str]:
        log.captcha('Solving Captcha...')
        self.s = time.time()

        while True:
            keys = ['url', 'sitekey', 'api_key', 'rqdata']
            values = [url, sitekey, self.api_key, rqdata]

            payload = {k: v for k, v in zip(keys, values) if (lambda x: x != "")(v)}

            try:
                response = requests.post("http://solver.dexv.lol:1000/api/solve_hcap", json=payload)
                data = response.json()
                if 'solved' in data:
                    answer = data['solved']
                    self.rn = str(time.time() - self.s)
                    log.captcha(f"Solved - {answer[:40]} - Time: {self.rn[:5]}")
                    return answer
                else:
                    log.failure(f"Failed To Solve - {data}", "Captcha")
                    break
            except requests.RequestException as e:
                log.failure(f"Failed To Solve - {e}", "Captcha")
                continue
    
    def get_balance(self) -> None:
        key: str = "DEXV-ulinfr-eoygs8-kr763i-nl3mt7"
        result = requests.get(f"http://solver.dexv.lol:1000/api/get_balance", json={"key": key})
        log.captcha(f"Balance: ${result.json()['balance']}")
