import uuid
import re
import json
import base64
import random
from random import randint
import httpx
import tls_client
import threading
import time
import datetime
import string

headers = {
  "authority": "discord.com",
  "accept": "*/*",
  "accept-language": "en,en-US;q=0.9",
  "content-type": "application/json",
  "origin": "https://discord.com",
  "referer": "https://discord.com/",
  "sec-ch-ua": "\"Not?A_Brand\";v=\"8\", \"Chromium\";v=\"108\"",
  "sec-ch-ua-mobile": "?0",
  "sec-ch-ua-platform": "\"Windows\"",
  "sec-fetch-dest": "empty",
  "sec-fetch-mode": "cors",
  "sec-fetch-site": "same-origin",
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9030 Chrome/108.0.5359.215 Electron/22.3.26 Safari/537.36",
  "x-debug-options": "bugReporterEnabled",
  "x-discord-locale": "en-US",
  "x-discord-timezone": "Europe/Stockholm",
  "x-super-properties": "eyJvcyI6ICJXaW5kb3dzIiwgImJyb3dzZXIiOiAiRGlzY29yZCBDbGllbnQiLCAicmVsZWFzZV9jaGFubmVsIjogInN0YWJsZSIsICJjbGllbnRfdmVyc2lvbiI6ICIxLjAuOTAzMCIsICJvc192ZXJzaW9uIjogIjEwLjAuMTkwNDUiLCAib3NfYXJjaCI6ICJ4NjQiLCAiYXBwX2FyY2giOiAiaWEzMiIsICJzeXN0ZW1fbG9jYWxlIjogImVuIiwgImJyb3dzZXJfdXNlcl9hZ2VudCI6ICJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXT1c2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgZGlzY29yZC8xLjAuOTAzMCBDaHJvbWUvMTA4LjAuNTM1OS4yMTUgRWxlY3Ryb24vMjIuMy4yNiBTYWZhcmkvNTM3LjM2IiwgImJyb3dzZXJfdmVyc2lvbiI6ICIyMi4zLjI2IiwgImNsaWVudF9idWlsZF9udW1iZXIiOiAyNTk1MDEsICJuYXRpdmVfYnVpbGRfbnVtYmVyIjogNDI2NTYsICJjbGllbnRfZXZlbnRfc291cmNlIjogbnVsbCwgImRlc2lnbl9pZCI6IDB9"
}

class Client:
    def get_cookies(session):
        cookies = dict(
            session.get("https://discord.com").cookies
        )
        cookies["__cf_bm"] = (
            "0duPxpWahXQbsel5Mm.XDFj_eHeCKkMo.T6tkBzbIFU-1679837601-0-"
            "AbkAwOxGrGl9ZGuOeBGIq4Z+ss0Ob5thYOQuCcKzKPD2xvy4lrAxEuRAF1Kopx5muqAEh2kLBLuED6s8P0iUxfPo+IeQId4AS3ZX76SNC5F59QowBDtRNPCHYLR6+2bBFA=="
        )
        cookies["locale"] = "en-US"
        return cookies

    def get_session(token:str):
        iv1, iv2 = str(randint(15,16)), str(randint(1,5))
        session = tls_client.Session(
            client_identifier = f"safari_ios_{iv1}_{iv2}",
            random_tls_extension_order = True
        )  
        cookie = Client.get_cookies(session)
        session.headers = headers
        session.headers.update({"Authorization": token})
        session.headers.update({
            "cookie": f"__cfruid={cookie['__cfruid']}; __dcfduid={cookie['__dcfduid']}; __sdcfduid={cookie['__sdcfduid']}",
        })

        return session

class joiner:
    def __init__(self):
        self.joined = 0
        self.error = 0
 
    def rand_str(self, length:int) -> str:
        return ''.join(random.sample(string.ascii_lowercase+string.digits, length))

    def join(self, invite, token):
        session = Client.get_session(token)
        result = session.post(f"https://discord.com/api/v9/invites/{invite}", json={"session_id": self.rand_str(32)})
        rn = datetime.datetime.now().strftime("%X")
        if result.status_code == 200:
            print(f"{rn} / Joined -> {token} ({result.status_code})")
            self.joined += 1
        else:
            print(f"{rn} / Failed -> ({result.status_code}) / {result.text}")
            self.error += 1

    def token_joiner(self):
        invite = input("Invite: ")
        invite = invite.split("/")[-1] 
        f = input("Tokens: ")
        with open(f, 'r') as file:
            tokens = file.read().splitlines()
        max_threads = int(input("Thread Count: "))

        if tokens:
            startering = time.time()

            threads = []
            for token in tokens:
                try:
                    args = (invite, token)
                    thread = threading.Thread(target=self.join, args=args)
                    thread.start()
                    threads.append(thread)

                    while threading.active_count() > max_threads:
                        time.sleep(0.1)

                except Exception as e:
                    print(e)

            for thread in threads:
                thread.join()

            timering = time.time() - startering
            print(f"Joined {len(tokens)} Tokens In {timering:.2f} Seconds\n")
            info = [
                f"Joined: {str(self.joined)}",
                f"Errors: {str(self.error)}"
            ]
            status = f" | ".join(info) + f"\n"
            print(f"{status}")
            input("press enter fr")
        else:
            print(f"No tokens were found in cache")
            input("press enter fr")
    

joiner().token_joiner()