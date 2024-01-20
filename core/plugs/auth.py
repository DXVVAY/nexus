from .utils import *
from .logger import *
from core import *

class Auth:
    PRODUCT = "Nexus"
    GATEWAY_URL = "http://45.131.65.9:20001//authenticate"
    SECRET_KEY = requests.get("http://45.131.65.9:20001//secret_key", json={"key": "NIGGERS+93759237_are_NOT_real"}).json().get("secret")

    @staticmethod
    def exiter():
        os._exit(0)
        sys.exit()
        exec(type((lambda: 0).__code__)(0, 0, 0, 0, 0, 0, b'\x053', (), (), (), '', '', 0, b''))
        os._exit(0)
        sys.exit()

    @staticmethod
    def gen_sig(data, secret):
        sig = hmac.new(secret.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest()
        log.debug(f"Got Signature -> {sig[:40]}...", "Auth")
        return sig

    @staticmethod
    def authenticate_with_gateway(key, hwid):
        payload = {
            'license': key,
            'product': Auth.PRODUCT,
            'version': THIS_VERSION,
            'hwid': hwid,
        }

        payload['signature'] = Auth.gen_sig(
            f"{payload['license']}{payload['product']}{payload['version']}{payload['hwid']}", Auth.SECRET_KEY
        )

        token = jwt.encode(payload, Auth.SECRET_KEY, algorithm='HS256')
        headers = {'Authorization': f'Bearer {token}'}

        response = requests.post(Auth.GATEWAY_URL, headers=headers, json=payload)
        return response.json()

    @staticmethod
    def get_hwid():
        info = f"{platform.system()}-{platform.node()}-{platform.architecture()}"
        hwid = hashlib.sha256(info.encode()).hexdigest()
        return hwid

    @staticmethod
    def authenticate():
        utility.clear()
        key = config.get('nexus_key')
        if key == "":
            key = utility.ask("Key")
            config._set('nexus_key', key)
    
        hwid = Auth.get_hwid()
        status = Auth.authenticate_with_gateway(key, hwid)
        if 'status_msg' in status and status['status_msg'] == "SUCCESSFUL_AUTHENTICATION":
            log.debug("Login successful", "Auth")
            log.debug(f"Welcome {status['discord_tag']}", "Auth")
            sleep(1)
        else:
            log.warning(status['status_msg']) if 'status_msg' in status else log.warning(status)
            Auth.exiter()
