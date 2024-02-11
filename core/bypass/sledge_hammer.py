from core import *

class Sledgehammer:
    def __init__(self, token: str, guild_id: str, channel_id: str, message_id: str) -> None:
        self.session = Client.get_session(token)
        self.token = token
        self.bot_id = "863168632941969438"
        self.session_id = utility.rand_str(32)
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.message_id = message_id

    def get_captcha(self):
        g = get_ephermal(self.token, self.bot_id, "Verify yourself to gain access to the server")
        thread = threading.Thread(target=g.run)
        thread.start()
        self.start()

        while not g.open:
            time.sleep(1)

        thread.join()

        return g.message

    def submit(self, answer: str):
        result = self.session.post("https://discord.com/api/v9/interactions",json={
            "type": 3,
            "nonce": utility.get_nonce(),
            "guild_id": self.guild_id,
            "channel_id": self.channel_id,
            "message_flags": 64,
            "message_id": self.message_id,
            "application_id": self.bot_id,
            "session_id": self.session_id,
            "data": {
                "component_type": 3,
                "custom_id": "verificationRequest.en",
                "type": 3,
                "values": [
                    answer
                ]
            }
        })
        log.success(f"{self.token[:50]}", "Pressed") if result.status_code == 204 else log.errors(self.token, result.text, result.status_code)

    def start(self):
        result = self.session.post("https://discord.com/api/v9/interactions",json={
            "type": 3,
            "nonce": utility.get_nonce(),
            "guild_id": self.guild_id,
            "channel_id": self.channel_id,
            "message_flags": 0,
            "message_id": self.message_id,
            "application_id": self.bot_id,
            "session_id": self.session_id,
            "data": {
                "component_type": 2,
                "custom_id": "startVerification.en"
            }
        })
        log.success(f"{self.token[:50]}", "Pressed") if result.status_code == 204 else log.errors(self.token, result.text, result.status_code)

    def get_answer(self, embed: str):
        desc = embed["embeds"][0]["description"]
        object = re.search(r'select the (.*?) on the', desc).group(1)[2:][:-2].lower().split()
        object = f"{object[0]}{''.join(word.capitalize() for word in object[1:])}"
        return next((option["value"] for option in embed["components"][0]["components"][0]["options"] if option["value"] == object), None)

    def verify(self):
        embed = self.get_captcha()
        answer = self.get_answer(embed)
        self.message_id = embed["id"]
        self.submit(answer)
        return answer

def hammer(guild_id: str, channel_id: str, message_id: str, token: str):
    s = time.time()
    hammer = Sledgehammer(token=token, guild_id=guild_id, channel_id=channel_id, message_id=message_id)
    answer = hammer.verify()
    rn = str(time.time() - s)
    log.success(f"{token[:40]} - Answer: {answer} - Time: {rn[:5]}", "Bypassed")

def sledge_hammer(link: str):
    set_title("Sledge Hammer Bypass")
    message = utility.message_info(link)
    guild_id = message["guild_id"]
    channel_id = message["channel_id"]
    message_id = message["message_id"]
    utility.run_threads(max_threads="1", func=hammer, args=[guild_id, channel_id, message_id])