from core import *

class get_ephermal(websocket.WebSocketApp):
    def __init__(self, token: str, bot_id: str, text: str):
        self.text: str = text
        self.packets_recv: int = 0
        self.message: dict = {}
        self.bot_id: str = str(bot_id)
        self.token: str = token
        self.open: bool = False
        self.socket_headers: Dict[str, str] = {
            "Accept-Language": headers["accept-language"],
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
            "User-Agent": headers["user-agent"],
        }
        super().__init__(
            "wss://gateway.discord.gg/?encoding=json&v=9",
            header=self.socket_headers,
            on_open=self.sock_open,
            on_message=self.sock_message
        )
        
    def run(self) -> dict:
        self.run_forever()
        self.open = True
        return self.message
    
    def sock_open(self, ws: websocket.WebSocket):
        self.send(json.dumps({
            "op": 2,
            "d": {
                "token": self.token,
                "capabilities": 125,
                "properties": {
                    "os": "Windows",
                    "browser": "Chrome",
                    "device": "",
                    "system_locale": "sv-SE",
                    "browser_user_agent": headers["user-agent"],
                    "browser_version": "121.0",
                    "os_version": "10",
                    "referrer": "",
                    "referring_domain": "",
                    "referrer_current": "",
                    "referring_domain_current": "",
                    "release_channel": "stable",
                    "client_build_number": 264913,
                    "client_event_source": None
                },
                "presence": {
                    "status": random.choice(["online", "dnd", "idle"]),
                    "since": 0,
                    "activities": [{
                        "details": f"Nexus - Discord Exploit Tool",
                        "state": f"https://nexus.vin",
                        "name": "Nexus",
                        "type": 1,
                        "url": "https://nexus.vin"
                    }],
                    "afk": False
                },
                "compress": False,
                "client_state": {
                    "guild_hashes": {},
                    "highest_last_message_id": "0",
                    "read_state_version": 0,
                    "user_guild_settings_version": -1,
                    "user_settings_version": -1
                }
            }
        }))

    def sock_message(self, ws: websocket.WebSocket, message: str):
        decoded: dict = json.loads(message)
        if self.text in str(decoded):
            self.message = decoded["d"]
            self.close()

    def sock_close(self, ws: websocket.WebSocket, close_code: int, close_msg: str):
        pass

def sock_open(token: str, socket: websocket.WebSocket):
  socket.connect('wss://gateway.discord.gg/?encoding=json&v=9&compress=json')
  socket.send(
    json.dumps({
            "op": 2,
            "d": {
                "token": token,
                "capabilities": 125,
                "properties": {
                    "os": "Windows",
                    "browser": "Chrome",
                    "device": "",
                    "system_locale": "sv-SE",
                    "browser_user_agent": headers["user-agent"],
                    "browser_version": "121.0",
                    "os_version": "10",
                    "referrer": "",
                    "referring_domain": "",
                    "referrer_current": "",
                    "referring_domain_current": "",
                    "release_channel": "stable",
                    "client_build_number": 264913,
                    "client_event_source": None
                },
                "presence": {
                    "status": random.choice(["online", "dnd", "idle"]),
                    "since": 0,
                    "activities": [{
                        "details": f"Nexus - Discord Exploit Tool",
                        "state": f"https://nexus.vin",
                        "name": "Nexus",
                        "type": 1,
                        "url": "https://nexus.vin"
                    }],
                    "afk": False
                },
                "compress": False,
                "client_state": {
                    "guild_hashes": {},
                    "highest_last_message_id": "0",
                    "read_state_version": 0,
                    "user_guild_settings_version": -1,
                    "user_settings_version": -1
                }
            }
        }))

def online(token: str):
    try:
        ws = websocket.WebSocket()
        ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
        ws.send(json.dumps({"op": 2, "d": {"token": token, "properties": {"$os": "Discord iOS", "$browser": "Chrome", "$device": ""}}, "s": None, "t": None}))
        act = [{"type": 0, "timestamps": {"start": utility.rand_time()}, "name": random.choice(["Battlerite", "League of Legends", "PLAYERUNKNOWN'S BATTLEGROUNDS", "Counter-Strike: Global Offensive", "Overwatch", "Minecraft", "World of Warcraft", "Grand Theft Auto V", "Tom Clancy's Rainbow Six Siege", "Rocket League"])}] if not config.get("token_rpc") else [{"details": "Nexus - Discord Exploit Tool", "state": "https://nexus.vin", "name": "Nexus", "type": 1, "url": "https://nexus.vin"}]
        ws.send(json.dumps({"op": 3, "d": {"since": 0, "activities": act, "status": random.choice(["online", "dnd", "idle"]), "afk": False}}))
    except:
        online(token)