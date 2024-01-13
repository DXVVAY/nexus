import requests
import hashlib
import hmac
import jwt
import os
import platform
from ab5 import vgratient
from pystyle import Center
from logger import logger
import subprocess


match platform.uname().system:
    case "Windows":
        clear = lambda: os.system('cls')
    case _:
        clear = lambda: os.system('clear')

class Auth:
    VERSION = "1.0.0"
    PRODUCT = "Nexus"
    GATEWAY_URL = "http://45.131.65.9:5000//authenticate"
    SECRET_KEY = "Niggatronnigga[[23[4]23[][]]7[[7]"

    ASCII = """
                        ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
                        ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
                        ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
                        ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
                        ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
                        ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
    """

    WHITE = "\u001b[37m"
    MAGENTA = "\033[38;5;97m"
    RED = "\u001b[31m"
    GREEN = "\u001b[32m"
    YELLOW = "\u001b[33m";
    PINK = "\033[38;5;176m"
    START_COLOR = [111, 70, 133]
    END_COLOR = [218, 112, 214]



    @staticmethod
    def generate_signature(data, secret):
        return hmac.new(secret.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest()

    @staticmethod
    def authenticate_with_gateway(key, hwid):
        payload = {
            'license': key,
            'product': Auth.PRODUCT,
            'version': Auth.VERSION,
            'hwid': hwid,
        }

        payload['signature'] = Auth.generate_signature(
            f"{payload['license']}{payload['product']}{payload['version']}{payload['hwid']}", Auth.SECRET_KEY
        )

        token = jwt.encode(payload, Auth.SECRET_KEY, algorithm='HS256')
        headers = {'Authorization': f'Bearer {token}'}

        response = requests.post(Auth.GATEWAY_URL, headers=headers, json=payload)
        return response.json()

    @staticmethod
    def banner():
        clear()
        print(Center.XCenter(vgratient(Auth.ASCII, Auth.START_COLOR, Auth.END_COLOR)))

    @staticmethod
    def get_hwid():
        info = f"{platform.system()}-{platform.node()}-{platform.architecture()}"
        hwid = hashlib.sha256(info.encode()).hexdigest()
        return hwid

    @staticmethod
    def main():
        Auth.banner()
        key = input(f"{Auth.PINK}[{Auth.MAGENTA}Key{Auth.PINK}]{Auth.WHITE} -> ")
        hwid = Auth.get_hwid()
        status = Auth.authenticate_with_gateway(key, hwid)
        if status['status_msg'] == "SUCCESSFUL_AUTHENTICATION":
            logger.success("Login successful")
            logger.welcome(status['discord_tag'])
            asd = input("")
        else:
            Auth.handle_error(status['status_msg'])

    @staticmethod
    def handle_error(status_msg):
        error_messages = {
            "MAX_IP_CAP": "You have reached the maximum number of allowed IP addresses!",
            "INVALID_LICENSE": "Your license key is invalid!",
            "MAX_HWID_CAP": "You have reached the maximum number of allowed HWIDs!",
        }

        error_message = error_messages.get(status_msg, "Something went wrong!")
        print(error_message)

if __name__ == "__main__":
    Auth.main()