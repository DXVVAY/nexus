from .logger import *
from core import *

file = os.path.join('scraped.txt')

class WebSocket(websocket.WebSocketApp): 
    def __init__(self, token, guild_id, channel_id, typ="ids"):
        self.type = typ
        self.MAX_ITER = 10
        self.token = token
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.current_session = Client.get_session("")
        self.socket_headers = {
            "Accept-Language": self.current_session.headers["accept-language"],
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
            "User-Agent": self.current_session.headers["user-agent"],
        }
        super().__init__(
            "wss://gateway.discord.gg/?encoding=json&v=9",
            header=self.socket_headers,
            on_open=lambda ws: self.sock_open(ws),
            on_message=lambda ws, msg: self.sock_message(ws, msg),
            on_close=lambda ws, close_code, close_msg: self.sock_close(
                ws, close_code, close_msg
            ),
        )
        self.endScraping = False
        self.guilds = {}
        self.members: list[str] = []
        self.ranges = [[0]]
        self.lastRange = 0
        self.packets_recv = 0
        self.msgs = []
        self.d = 1
        self.iter = 0
        self.big_iter = 0
        self.finished = False

    def get_ranges(self, index, multiplier, memberCount):
        initialNum = int(index * multiplier)
        rangesList = [[initialNum, initialNum + 99]]
        if memberCount > initialNum + 99:
            rangesList.append([initialNum + 100, initialNum + 199])
        if [0, 99] not in rangesList:
            rangesList.insert(0, [0, 99])
        return rangesList

    def parse_member(self, response):
        memberdata = {
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
            memberdata["types"].append(chunk["op"])
            if chunk["op"] in ("SYNC", "INVALIDATE"):
                memberdata["locations"].append(chunk["range"])
                if chunk["op"] == "SYNC":
                    memberdata["updates"].append(chunk["items"])
                else:
                    memberdata["updates"].append([])
            elif chunk["op"] in ("INSERT", "UPDATE", "DELETE"):
                memberdata["locations"].append(chunk["index"])
                if chunk["op"] == "DELETE":
                    memberdata["updates"].append([])
                else:
                    memberdata["updates"].append(chunk["item"])
        return memberdata

    def find_most_reoccuring(self, list):
        return max(set(list), key=list.count)

    def run(self) -> list[str]:
        try:
            self.run_forever()
            self.finished = True
            return self.members
        except Exception as e:
            print(e)
            pass

    def scrape_users(self):
        if self.endScraping == False:
            self.send(
                '{"op":14,"d":{"guild_id":"'
                + self.guild_id
                + '","typing":true,"activities":true,"threads":true,"channels":{"'
                + self.channel_id
                + '":'
                + json.dumps(self.ranges)
                + "}}}"
            )

    def sock_open(self, ws):
        self.send(
            '{"op":2,"d":{"token":"'
            + self.token
            + '","capabilities":125,"properties":{"os":"Windows","browser":"Firefox","device":"","system_locale":"it-IT","browser_user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0","browser_version":"94.0","os_version":"10","referrer":"","referring_domain":"","referrer_current":"","referring_domain_current":"","release_channel":"stable","client_build_number":103981,"client_event_source":null},"presence":{"status":"online","since":0,"activities":[],"afk":false},"compress":false,"client_state":{"guild_hashes":{},"highest_last_message_id":"0","read_state_version":0,"user_guild_settings_version":-1,"user_settings_version":-1}}}'
        )

    def heart_beat(self, interval):
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
                log.scraper(f"Scraping {len(self.members)} members")

                if self.d == len(self.members):
                    self.iter += 1
                    if self.iter == self.MAX_ITER:
                        log.scraper(f"Scraping {len(self.members)} members")
                        self.endScraping = True
                        self.close()
                        return

                self.d = int(self.find_most_reoccuring(self.msgs))

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
                                            obj = {
                                                "tag": mem["user"]["username"]
                                                + "#"
                                                + mem["user"]["discriminator"],
                                                "id": mem["user"]["id"],
                                            }
                                            if not mem["user"].get("bot"):
                                                if self.type == "ids":
                                                    self.members.append(
                                                        str(mem["user"]["id"])
                                                    )
                                                else:
                                                    self.members.append(
                                                        str(mem["user"]["username"])
                                                    )
                        elif index == "UPDATE":
                            for item in parsed["updates"][elem]:
                                if isinstance(item, dict) and "member" in item:
                                    mem = item["member"]
                                    obj = {
                                        "tag": mem["user"]["username"]
                                        + "#"
                                        + mem["user"]["discriminator"],
                                        "id": mem["user"]["id"],
                                    }
                                    if not mem["user"].get("bot"):
                                        if self.type == "ids":
                                            self.members.append(str(mem["user"]["id"]))
                                        else:
                                            self.members.append(str(mem["user"]["username"]))

                        self.lastRange += 1
                        self.ranges = self.get_ranges(
                            self.lastRange,
                            100,
                            self.guilds[self.guild_id]["member_count"],
                        )
                        time.sleep(0.1)
                        self.scrape_users()

                if self.endScraping:
                    self.close()
        except Exception as e:
            print(e)

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
    
    token = utility.clean_token(config.get_random_token())
    
    users = WebSocket(token, guild_id, channel_id, typ).run()
    with open(file, "w", encoding="utf-8") as f:
        for user in users:
            f.write(f"{user}\n")
    
    print()
    log.info(f"Scraped {len(users)} {typ}", "Scraper")