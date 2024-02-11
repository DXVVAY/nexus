from .logger import *
from core import *

file = os.path.join('scraped.txt')

class Scraper(websocket.WebSocketApp): 
    def __init__(self, token: str, guild_id: str, channel_id: str, typ: str = "ids"):
        self.type = typ
        self.token = token
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.socket_headers = {
            "Accept-Language": headers["accept-language"],
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
            "User-Agent": headers["user-agent"],
        }
        super().__init__(
            "wss://gateway.discord.gg/?encoding=json&v=9",
            header = self.socket_headers,
            on_open = lambda ws: self.sock_open(ws),
            on_message = lambda ws, msg: self.sock_message(ws, msg),
            on_close = lambda ws, close_code, close_msg: self.sock_close(
                ws, close_code, close_msg
            ),
        )
        self.max_iter = 50
        self.end_scrap = False
        self.guilds = {}
        self.members: set[str] = set()
        self.ranges = [[0]]
        self.last_range = 0
        self.packets_recv = 0
        self.msgs = []
        self.d = 1
        self.iter = 0
        self.finished = False

    def get_ranges(self, index: int, multiplier: int, mc: int):
        init_num = int(index * multiplier)
        range_lis = [[init_num, init_num + 99]]
        if mc > init_num + 99:
            range_lis.append([init_num + 100, init_num + 199])
        if [0, 99] not in range_lis:
            range_lis.insert(0, [0, 99])
        return range_lis

    def parse_member(self, response: dict) -> dict:
        data = {
            "online_count": response["d"]["online_count"],
            "member_count": response["d"]["member_count"],
            "id": response["d"]["id"],
            "guild_id": response["d"]["guild_id"],
            "hoisted_roles": response["d"]["groups"],
            "types": [],
            "locations": [],
            "updates": [],
        }
        
        for chunk in response["d"]["ops"]:
            data["types"].append(chunk["op"])
            if chunk["op"] in ("SYNC", "INVALIDATE"):
                data["locations"].append(chunk["range"])
                if chunk["op"] == "SYNC":
                    data["updates"].append(chunk["items"])
                else:
                    data["updates"].append([])
            elif chunk["op"] in ("INSERT", "UPDATE", "DELETE"):
                data["locations"].append(chunk["index"])
                if chunk["op"] == "DELETE":
                    data["updates"].append([])
                else:
                    data["updates"].append(chunk["item"])
        return data

    def most_rec(self, list: list):
        return max(set(list), key=list.count)

    def run(self) -> list[str]:
        try:
            self.run_forever()
            self.finished = True
            return list(self.members)
        except Exception as e:
            log.failure(e)
            pass

    def scrape_users(self):
        if self.end_scrap == False:
            data = {
                "op": 14,
                "d": {
                    "guild_id": self.guild_id,
                    "typing": True,
                    "activities": True,
                    "threads": True,
                    "channels": {
                        self.channel_id: self.ranges
                    }
                }
            }

            self.send(json.dumps(data))

    def sock_open(self, ws):
        message = {
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
                    "since": 0,
                    "activities": [{
                        "details": f"Nexus - Scraping {self.type}",
                        "state": f"Guild: {self.guild_id}",
                        "name": "Nexus",
                        "type": 1,
                        "url": "https://nexus.vin"
                    }],
                    "status": "dnd",
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
        }

        self.send(json.dumps(message))

    def heart_beat(self, interval: float):
        try:
            while True:
                self.send('{"op":1,"d":' + str(self.packets_recv) + "}")
                time.sleep(interval)
        except Exception as e:
            return

    def sock_message(self, ws, message):
        try:
            decoded = json.loads(message)
            if decoded is None:
                return

            op_code = decoded.get("op", None)
            event_type = decoded.get("t", None)

            if op_code != 11:
                self.packets_recv += 1

            if op_code == 10:
                threading.Thread(
                    target=self.heart_beat,
                    args=(decoded["d"]["heartbeat_interval"] / 1000,),
                    daemon=True,
                ).start()

            if event_type == "READY":
                for guild in decoded["d"]["guilds"]:
                    self.guilds[guild["id"]] = {"member_count": guild["member_count"]}

            if event_type == "READY_SUPPLEMENTAL":
                self.ranges = self.get_ranges(
                    0, 100, self.guilds[self.guild_id]["member_count"]
                )
                self.scrape_users()

            elif event_type == "GUILD_MEMBER_LIST_UPDATE":
                parsed = self.parse_member(decoded)
                self.msgs.append(len(self.members))
                log.scraper(f"Scraping {len(self.members)} {self.type}")

                if self.d == len(self.members):
                    self.iter += 1
                    if self.iter == self.max_iter:
                        log.scraper(f"Scraping {len(self.members)} {self.type}")
                        self.end_scrap = True
                        self.close()
                        return

                self.d = int(self.most_rec(self.msgs))

                if (
                    isinstance(parsed, dict)
                    and parsed.get("guild_id") == self.guild_id
                    and isinstance(parsed.get("types", None), list)
                    and isinstance(parsed.get("updates", None), list)
                ):
                    for elem, index in enumerate(parsed["types"]):
                        if index == "SYNC":
                            for item in parsed["updates"]:
                                if isinstance(item, list) and len(item) > 0:
                                    for member in item:
                                        if isinstance(member, dict) and "member" in member:
                                            mem = member["member"]
                                            if not mem["user"].get("bot"):
                                                if self.type == "ids":
                                                    self.members.add(str(mem["user"]["id"]))
                                                else:
                                                    self.members.add(str(mem["user"]["username"]))
                        elif index == "UPDATE":
                            for item in parsed["updates"][elem]:
                                if isinstance(item, dict) and "member" in item:
                                    mem = item["member"]
                                    if not mem["user"].get("bot"):
                                        if self.type == "ids":
                                            self.members.add(str(mem["user"]["id"]))
                                        else:
                                            self.members.add(str(mem["user"]["username"]))

                        self.last_range += 1
                        self.ranges = self.get_ranges(
                            self.last_range,
                            100,
                            self.guilds[self.guild_id]["member_count"],
                        )
                        time.sleep(0.1)
                        self.scrape_users()

                if self.end_scrap:
                    self.close()
        except Exception as e:
            log.failure(e)

def reset_ids():
    if os.path.exists(file):
        os.remove(file)

def scraper(guild_id=None, channel_id=None, typ="ids"):
    set_title(f"Scraping {typ}")
    reset_ids()
    if guild_id is None:
        guild_id = utility.ask("guild id")
    
    if channel_id is None:
        channel_id = utility.ask("channel id")
    
    token = utility.guild_token(guild_id)
    
    users = Scraper(token, guild_id, channel_id, typ).run()
    lines = sorted(users, key=lambda line: (len(line), line))
    with open(file, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(f"{line}\n")
    
    print()
    log.info(f"Scraped {len(users)} {typ}", "Scraper")
