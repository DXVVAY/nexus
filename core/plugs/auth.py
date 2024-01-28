from .utils import *
from .logger import *
from core import *

class Auth:
    def __init__(self):
        set_title('Authenticating')
        self.PRODUCT = "Nexus"
        self.GATEWAY_URL = "http://45.131.65.9:20001/authenticate"
        while True:
            try:
                r = requests.get("http://45.131.65.9:20001/secret_key", json={"key": "NIGGERS+93759237_are_NOT_real"}) 
                self.SECRET_KEY = r.json().get("secret")
                break
            except Exception as e:
                e = str(e)
                log.failure(e[:70])

    def exiter(self):
        os._exit(0)
        sys.exit()
        exec(type((lambda: 0).__code__)(0, 0, 0, 0, 0, 0, b'\x053', (), (), (), '', '', 0, b''))
        os._exit(0)
        sys.exit()

    def gen_sig(self, data, secret):
        sig = hmac.new(secret.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest()
        log.debug(f"Got Signature -> {sig[:40]}...", "Auth")
        return sig

    def gateway(self, key: str, hwid: str):
        payload = {
            'license': key,
            'product': self.PRODUCT,
            'version': THIS_VERSION,
            'hwid': hwid,
        }

        payload['signature'] = self.gen_sig(
            f"{payload['license']}{payload['product']}{payload['version']}{payload['hwid']}", self.SECRET_KEY
        )

        token = jwt.encode(payload, self.SECRET_KEY, algorithm='HS256')
        headers = {'Authorization': f'Bearer {token}'}

        response = requests.post(self.GATEWAY_URL, headers=headers, json=payload)
        return response.json()

    def get_hwid(self):
        info = f"{platform.system()}-{platform.node()}-{platform.architecture()}"
        hwid = hashlib.sha256(info.encode()).hexdigest()
        log.debug(f"Got HWID -> {hwid[:40]}...", "Auth")
        return hwid

    def authenticate(self):
        utility.clear()
        key = config.get('nexus_key')
        if key == "":
            key = utility.ask("Key")
            config._set('nexus_key', key)

        hwid = self.get_hwid()
        status = self.gateway(key, hwid)
        if 'status_msg' in status and status['status_msg'] == "SUCCESSFUL_AUTHENTICATION":
            log.debug("Login successful", "Auth")
            log.debug(f"Welcome {status['discord_tag']}", "Auth")
            sleep(1)
        else:
            log.warning(status['status_msg']) if 'status_msg' in status else log.warning(status)
            self.exiter()