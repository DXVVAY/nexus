from core import *

class get_ephermal(websocket.WebSocketApp):
    def __init__(self, token: str, bot_id: str, text: str):
        self.text = text
        self.packets_recv = 0
        self.message: dict = {}
        self.bot_id = str(bot_id)
        self.token = token
        self.open = False
        self.create_id = None
        self.socket_headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9030 Chrome/121.0.6167.85 Electron/22.3.26 Safari/537.36"
        }
        super().__init__(
            "wss://gateway.discord.gg/?encoding=json&v=9",
            header = self.socket_headers,
            on_open = self.sock_open,
            on_message = self.sock_message
        )
        
    def run(self) -> dict:
        self.run_forever()
        self.open = True
        return self.message
    
    def sock_open(self, ws):
        self.send(json.dumps({
            "op": 2,
            "d": {
                "token": self.token,
                "capabilities": 125,
                "properties": {
                    "os": "Windows",
                    "browser": "Firefox",
                    "device": "",
                    "system_locale": "sv-SE",
                    "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
                    "browser_version": "94.0",
                    "os_version": "10",
                    "referrer": "",
                    "referring_domain": "",
                    "referrer_current": "",
                    "referring_domain_current": "",
                    "release_channel": "stable",
                    "client_build_number": 103981,
                    "client_event_source": None
                },
                "presence": {
                    "status": "online",
                    "since": 0,
                    "activities": [],
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

    def sock_message(self, ws, message):
        decoded = json.loads(message)
        if self.text in str(decoded):
            self.message = decoded["d"]
            self.close()

    def sock_close(self, ws, close_code, close_msg):
        pass

def sock_open(token: str, socket):
  socket.connect('wss://gateway.discord.gg/?encoding=json&v=9&compress=json')
  socket.send(
    json.dumps({
            "op": 2,
            "d": {
                "token": token,
                "capabilities": 125,
                "properties": {
                    "os": "Windows",
                    "browser": "Firefox",
                    "device": "",
                    "system_locale": "sv-SE",
                    "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
                    "browser_version": "94.0",
                    "os_version": "10",
                    "referrer": "",
                    "referring_domain": "",
                    "referrer_current": "",
                    "referring_domain_current": "",
                    "release_channel": "stable",
                    "client_build_number": 103981,
                    "client_event_source": None
                },
                "presence": {
                    "status": "online",
                    "since": 0,
                    "activities": [],
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
        device = utility.randp({"Discord iOS": 25, "Windows": 75})
        ws.send(json.dumps({
            "op": 2,
            "d": {
                "token": token,
                "properties": {
                    "$os": device,
                    "$browser": device,
                    "$device": device
                }
            },
            "s": None,
            "t": None
        }, indent=4))

        if config.get("token_rpc"):
            act = [{
                        "details": f"Nexus - Discord Exploit Tool",
                        "state": f"https://nexus.vin",
                        "name": "Nexus",
                        "type": 1,
                        "url": "https://nexus.vin"
                    }]
        else:
            act = [{"type": 0, "timestamps": {"start": utility.rand_time()}, "name": utility.randp({"Battlerite": 10, "League of Legends": 10, "PLAYERUNKNOWN'S BATTLEGROUNDS": 10, "Counter-Strike: Global Offensive": 10, "Overwatch": 10, "Minecraft": 15, "World of Warcraft": 5, "Grand Theft Auto V": 10, "Tom Clancy's Rainbow Six Siege": 10, "Rocket League": 10}), }]
        payload = json.dumps({
            "op": 3,
            "d": {
                "since": 0,
                "activities": act,
                "status": utility.randp({"online": 35, "dnd": 45, "idle": 20}),
                "afk": False
            }
        }, indent=4)
        ws.send(payload)
    except Exception as e:
        log.failure(e)
        online(token)