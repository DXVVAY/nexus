from core import *

class nexcha:
    def __init__(self):
        self.api_key = "DEXV-rhdgva-82tk4q-g8nlj6-rpgmw0"
        self.start_time = None

    def solve(self, url, sitekey, rqdata=""):
        log.captcha('Solving Captcha...')
        self.s = time.time()

        while True:
            if rqdata != "":
                payload = {
                    'url': url,
                    'sitekey': sitekey,
                    'api_key': self.api_key,
                    'rqdata':rqdata,
                }
            else:
                payload = {
                    'url': url,
                    'sitekey': sitekey,
                    'api_key': self.api_key,
                }

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