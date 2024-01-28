from core import *

class capsolver:
    def __init__(self):
        self.api_key = config.get("captcha_key")
        self.s = None

    def solve(self, url: str, sitekey: str, rqdata: str):
        log.captcha('Solving Captcha...')
        self.s = time.time()
        json = {
            "clientKey": self.api_key,
            "task": {
                "type": "HCaptchaTask",
                "websiteURL": url,
                "websiteKey": sitekey,
                "enterprisePayload": {
                  "rqdata": rqdata
                },
                "proxy": "http://3e8j8h0vylsx49g:54nw544u7iglpsm@rp.proxyscrape.com:6060",
            }
        }

        result = requests.post('https://api.capsolver.com/createTask', json=json)
        try:
            taskid = result.json()['taskId']
            log.captcha(f"Task ID: {taskid}")
        except:
            print('Error: {}'.format(result.json()['errorDescription']))
            return 

        json = {"clientKey": self.api_key, "taskId": taskid}
        while True:
            time.sleep(1.5)
            result = requests.post('https://api.capsolver.com/getTaskResult', json=json)
            if result.json()['status'] == 'ready':
                key = result.json()['solution']['gRecaptchaResponse']
                self.rn = str(time.time() - self.s)
                log.captcha(f"Solved - {key[:40]} - Time: {self.rn[:5]}")
                return key
            else:
                continue

    
    def get_balance(self):
        result = requests.post(f"https://api.capsolver.com/getBalance", json={"clientKey": self.api_key})
        log.captcha(f"Balance: ${result.json()['balance']}")