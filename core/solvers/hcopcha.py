from core import *

class hcopcha: 
    def __init__(self):
        self.api_key = config.get("captcha_key")
        self.s = None

    def solve(self, url: str, sitekey: str, rqdata: str):
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
                        id = response.json()['task_id']
                        log.captcha(f"Task ID: {id}")
                        while True:
                            awnser = requests.post(f"https://api.hcoptcha.online/api/getTaskData", json={
                                	"api_key": self.api_key,
                                	"task_id": id
                                })
                            if awnser.json()["task"]["state"] == "completed":
                               key = awnser.json()["task"]["captcha_key"]
                               self.rn = str(time.time() - self.s)
                               log.captcha(f"Solved - {key[:40]} - Time: {self.rn[:5]}")
                               return key
                    else:  
                        log.failure(f"Failed To Solve - {response.json()}", "Captcha")
                        continue
                    
                except Exception as e:
                    log.failure(f"Failed To Solve - {e}", "Captcha")        
                    continue
    
    def get_balance(self):
        result = requests.post("https://api.hcoptcha.online/api/getUserData", json={"api_key": solver_key})
        print(f"${result.json()['data']['balance']}")
        log.captcha(f"Balance: ${result.json()['data']['balance']}")