from core import *

class hcopcha: 
    def __init__(self):
        self.api_key: str = config.get("captcha_key")
        self.s: Optional[float] = None

    def solve(self, url: str, sitekey: str, rqdata: str) -> Optional[str]:
        log.captcha(f"Solving Captcha...")
        while True:
            self.s = time.time()
            payload = {
                "task_type": "hcaptchaEnterprise",
                "api_key": self.api_key,
                "data": {
                    "sitekey": sitekey,
                    "url": url,
                    "proxy": "http://3e8j8h0vylsx49g:54nw544u7iglpsm@rp.proxyscrape.com:6060",
                    "rqdata": rqdata
                }
            }

            try:
                response = requests.post("https://api.hcoptcha.online/api/createTask", json=payload)
                if "task_id" in response.text:
                    task_id = response.json()['task_id']
                    log.captcha(f"Task ID: {task_id}")
                    while True:
                        answer = requests.post(f"https://api.hcoptcha.online/api/getTaskData", json={
                            "api_key": self.api_key,
                            "task_id": task_id
                        })
                        if answer.json()["task"]["state"] == "completed":
                            key = answer.json()["task"]["captcha_key"]
                            self.rn = str(time.time() - self.s)
                            log.captcha(f"Solved - {key[:40]} - Time: {self.rn[:5]}")
                            return key
                else:  
                    log.failure(f"Failed To Solve - {response.json()}", "Captcha")
                    continue
                    
            except Exception as e:
                log.failure(f"Failed To Solve - {e}", "Captcha")        
                continue
    
    def get_balance(self) -> None:
        result = requests.post("https://api.hcoptcha.online/api/getUserData", json={"api_key": self.api_key})
        print(f"${result.json()['data']['balance']}")
        log.captcha(f"Balance: ${result.json()['data']['balance']}")