from core import *

class capsolver:
    def __init__(self):
        self.api_key: str = config.get("captcha_key")
        self.s: Optional[float] = None

    def solve(self, url: str, sitekey: str, rqdata: str) -> Optional[str]:
        log.captcha('Solving Captcha...')
        self.s = time.time()
        json_data = {
            "clientKey": self.api_key,
            "task": {
                "type": "HCaptchaTask",
                "websiteURL": url,
                "websiteKey": sitekey,
                "enterprisePayload": {
                    "rqdata": rqdata
                },
                "proxy": "https://ifpdbcmjj2inwin:4wyfy14mhtqljuw@rp.proxyscrape.com:6060",
            }
        }

        result = requests.post('https://api.capsolver.com/createTask', json=json_data)
        try:
            taskid = result.json()['taskId']
            log.captcha(f"Task ID: {taskid}")
        except Exception as e:
            log.captcha(f'Error: {str(e)}')
            return None

        json_data = {"clientKey": self.api_key, "taskId": taskid}
        while True:
            time.sleep(1.5)
            result = requests.post('https://api.capsolver.com/getTaskResult', json=json_data)
            if result.json()['status'] == 'ready':
                key = result.json()['solution']['gRecaptchaResponse']
                self.rn = str(time.time() - self.s)
                log.captcha(f"Solved - {key[:40]} - Time: {self.rn[:5]}")
                return key
            else:
                continue

    def get_balance(self) -> None:
        result = requests.post(f"https://api.capsolver.com/getBalance", json={"clientKey": self.api_key})
        log.captcha(f"Balance: ${result.json()['balance']}")
