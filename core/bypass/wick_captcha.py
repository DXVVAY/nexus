from core import *

class WickCap:
    def __init__(self, token: str, guild_id: str, channel_id: str, message_id: str) -> None:
        self.socket = websocket.WebSocket()
        self.session = Client.get_session(token)
        self.token = token
        self.bot_id = "536991182035746816"
        self.session_id = utility.rand_str(32)
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.message_id = message_id

    def get_cap(self, url: str):
        result = requests.post(f"http://wick.dexv.lol:2000/api/wick/solve", json={"url": url})
        if result.status_code == 200:
            data = result.json()
            if data["success"]:
                solve = data["solve"]
                return solve
            else:
                log.failure(f"Failed to solve wick captcha")
                return None
        else:
            log.failure(f"Failed to solve wick captcha")
            return None

    def get_embed(self):
        g = get_ephermal(self.token, self.bot_id, "Please type the captcha below to be able to access this server!")
        thread = threading.Thread(target=g.run)
        thread.start()
        self.start()

        while not g.open:
            time.sleep(1)

        thread.join()

        return g.message

    def finish(self, user_id: str, id: str, answer: str):
        result = self.session.post("https://discord.com/api/v9/interactions", json={
            "type": 5,
            "nonce": utility.get_nonce(),
            "guild_id": self.guild_id,
            "channel_id": self.channel_id,
            "application_id": self.bot_id,
            "session_id": self.session_id,
            "data": {
                "id": id,
                "custom_id": f"modalmmbrver_{user_id}",
                "components": [{
                    "type": 1,
                    "components": [{
                        "type": 4,
                        "custom_id": "answer",
                        "value": answer
                    }]
                }]
            }
        })
        log.success(f"{self.token[:50]}", "Pressed") if result.status_code == 204 else log.errors(self.token, result.text, result.status_code)

    def press(self, custom_id: str, message_flags: int):
        result = self.session.post("https://discord.com/api/v9/interactions", json={
            "type": 3,
            "nonce": utility.get_nonce(),
            "guild_id": self.guild_id,
            "channel_id": self.channel_id,
            "message_flags": message_flags,
            "message_id": self.message_id,
            "application_id": self.bot_id,
            "session_id": self.session_id,
            "data": {
                "component_type": 2,
                "custom_id": custom_id,
            }
        })
        log.success(f"{self.token[:50]}", "Pressed") if result.status_code == 204 else log.errors(self.token, result.text, result.status_code)

    def get_custom_id(self, messages: dict):
        for message in messages:
            for comp in message.get('components', []):
                for sub in comp.get('components', []):
                    if sub.get('label') == 'Verify':
                        return sub.get('custom_id')
        return None

    def answer(self, custom_id: str):
        sock_open(self.token, self.socket)
        self.press(custom_id, 64)
        while True:
            result = json.loads(self.socket.recv())
            if result['t'] == 'INTERACTION_SUCCESS':
                self.socket.close()
                return result['d']['id']

    def start(self):
        result = self.session.get(f"https://discord.com/api/v9/channels/{self.channel_id}/messages?limit=50")
        custom_id = self.get_custom_id(result.json())
        if custom_id is None:
            log.failure("No Verify button found")
            return
        self.press(custom_id, 0)

    def get_link(self, embed: str):
        url = embed["embeds"][0]["image"]["url"]
        custom_id = embed["components"][0]["components"][0]["custom_id"]
        return url, custom_id

    def verify(self):
        embed = self.get_embed()
        link, custom_id = self.get_link(embed)
        a = custom_id.split('_')
        token_id = a[-1] if len(a) > 2 else None
        self.message_id = embed["id"]
        id = self.answer(custom_id)
        answer = self.get_cap(link)
        self.finish(token_id, id, answer)
        return answer

def wick(guild_id: str, channel_id: str, message_id: str, token: str):
    s = time.time()
    wick = WickCap(token=token, guild_id=guild_id, channel_id=channel_id, message_id=message_id)
    answer = wick.verify()
    rn = str(time.time() - s)
    log.success(f"{token[:40]} - Answer: {answer} - Time: {rn[:5]}", "Bypassed")

def wick_captcha(link: str):
    set_title("Wick Captcha Bypass")
    message = utility.message_info(link)
    guild_id = message["guild_id"]
    channel_id = message["channel_id"]
    message_id = message["message_id"]
    utility.run_threads(max_threads="4", func=wick, args=[guild_id, channel_id, message_id])