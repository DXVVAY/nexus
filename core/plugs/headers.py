from .config import *
from .utils import *
from .logger import *
from core import *

# couldnt import them dont judge 
PINK = "\033[38;5;176m"
MAGENTA = "\033[38;5;97m"
WHITE = "\u001b[37m"
def make_menu(*options):
    print()
    for num, option in enumerate(options, start=1):
        label = f"    {PINK}[{MAGENTA}{num}{PINK}] {WHITE}{option}"
        print(label)
    print()

class IOS_headers:
    def __init__(self):
        s = time.time()
        self.build_number = None
        self.darwin_ver = self.get_darwin_version()
        self.iv1, self.iv2 = str(randint(15, 16)), str(randint(1, 5))
        self.app_version = self.get_app_version()
        set_title("Getting Discord IOS Info")
        log.info(f"Getting Discord IOS Info")
        self.build_number = self.get_build_number()
        self.user_agent = f"Discord/{self.build_number} CFNetwork/1402.0.8 Darwin/{self.darwin_ver}"
        log.info(self.build_number, "Build Number")
        log.info(self.darwin_ver, "Darwin Version")
        log.info(self.app_version, "App Version")
        log.info(self.user_agent, "User Agent")
        rn = str(time.time() - s)
        log.info(f"Successfully Built Headers In {rn[:5]} Seconds"); sleep(2)
        self.x_super_properties = self.mobile_xprops()
        self.dict = self.returner()

    def mobile_xprops(self):
        u = uuid.uuid4().hex
        vendor_uuid = f"{u[0:8]}-{u[8:12]}-{u[12:16]}-{u[16:20]}-{u[20:36]}"
        iphone_models = ["11,2", "11,4", "11,6", "11,8", "12,1", "12,3", "12,5", "12,8", "13,1", "13,2", "13,3", "13,4",
                         "14,2", "14,3", "14,4", "14,5", "14,6", "14,7", "14,8", "15,2", "15,3", ]
        return base64.b64encode(json.dumps({
            "os": "iOS",
            "browser": "Discord iOS",
            "device": "iPhone" + random.choice(iphone_models),
            "system_locale": "sv-SE",
            "client_version": self.app_version,
            "release_channel": "stable",
            "device_vendor_id": vendor_uuid,
            "browser_user_agent": "",
            "browser_version": "",
            "os_version": self.iv1 + "." + self.iv2,
            "client_build_number": self.build_number,
            "client_event_source": None,
            "design_id": 0
        }).encode()).decode()

    def get_build_number(self):
        while True:
            try:
                build_number = httpx.get(
                    f"https://discord.com/ios/{self.app_version}/manifest.json").json()["metadata"]["build"]
                break
            except:
                self.app_version = float(self.app_version) - 1
                continue

        return build_number

    def get_app_version(self):
        body = httpx.get(
            "https://apps.apple.com/us/app/discord-chat-talk-hangout/id985746746", headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            }).text

        return re.search(r'latest__version">Version (.*?)</p>', body).group(1)

    def get_darwin_version(self):
        darwin_wiki = httpx.get("https://en.wikipedia.org/wiki/Darwin_(operating_system)").text
        return re.search(r'Latest release.*?<td class="infobox-data">(.*?) /', darwin_wiki).group(1)

    def returner(self):
        return {
            "host": "discord.com",
            "x-debug-options": "bugReporterEnabled",
            "content-type": "application/json",
            "accept": "*/*",
            "user-agent": self.user_agent,
            "accept-language": "sv-SE",
            "x-discord-locale": "en-US",
            "x-super-properties": self.x_super_properties,
        }

    def __call__(self):
        return self.dict

class WIN_headers:
    def __init__(self):
        s = time.time()
        set_title("Getting Discord Desktop Info")
        log.info(f"Getting Discord Desktop Info")
        sleep(0.2)
        self.native_buildd = self.native_build()
        self.main_versiond = self.main_version()
        self.client_buildd = self.client_build()
        self.chrome = WIN_headers.chrome_version()
        self.electron = "22.3.26"
        self.safari = "537.36"
        self.os_version = "10.0.19045"
        self.user_agent = f"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/{self.safari} (KHTML, like Gecko) discord/{self.main_versiond} Chrome/{self.chrome} Electron/{self.electron} Safari/{self.safari}"
        log.info(self.client_buildd, "Build Number")
        log.info(self.native_buildd, "Native Build")
        log.info(self.main_versiond, "App Version")
        log.info(self.chrome, "Chrome Version")
        log.info(f"{self.user_agent[:60]}...", "User Agent")
        rn = str(time.time() - s)
        log.info(f"Successfully Built Headers In {rn[:5]} Seconds"); sleep(2)
        self.x_super_properties = self.desktop_xprops()
        self.dict = self.returner()

    @staticmethod
    def chrome_version() -> str:
        try:
            r = requests.get("https://versionhistory.googleapis.com/v1/chrome/platforms/linux/channels/stable/versions")
            data = json.loads(r.text)
            return data['versions'][0]['version']
        except Exception:
            return "108.0.5359.215"

    def desktop_xprops(self):
        return base64.b64encode(json.dumps({
            "os":"Windows",
            "browser":"Discord Client",
            "release_channel":"stable",
            "client_version":self.main_versiond,
            "os_version":self.os_version,
            "os_arch":"x64",
            "app_arch":"ia32",
            "system_locale":"en",
            "browser_user_agent":self.user_agent,
            "browser_version":self.electron,
            "client_build_number":self.client_buildd,
            "native_build_number":self.native_buildd,
            "client_event_source":None,
            "design_id":0
        }).encode()).decode()
    
    def native_build(self) -> int:
        return int(requests.get(
            "https://updates.discord.com/distributions/app/manifests/latest",
            params = {
                "install_id":'0',
                "channel":"stable",
                "platform":"win",
                "arch":"x86"
            },
            headers = {
                "user-agent": "Discord-Updater/1",
                "accept-encoding": "gzip"
        }).json()["metadata_version"])

    def client_build(self) -> int:
        page = requests.get("https://discord.com/app").text.split("app-mount")[1]
        assets = re.findall(r'src="/assets/([^"]+)"', page)[::-1]

        for asset in assets:
            js = requests.get(f"https://discord.com/assets/{asset}").text
            
            if "buildNumber:" in js:
                return int(js.split('buildNumber:"')[1].split('"')[0])

    def main_version(self) -> str:
        app = requests.get(
            "https://discord.com/api/downloads/distributions/app/installers/latest",
            params = {
                "channel":"stable",
                "platform":"win",
                "arch":"x86"
            },
            allow_redirects = False
        ).text

        return re.search(r'x86/(.*?)/', app).group(1)
    
    def returner(self):
        return {
            'authority': 'discord.com',
            'accept': '*/*',
            'accept-language': 'en,en-US;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'referer': 'https://discord.com/',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.user_agent,
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'en-US',
            'x-discord-timezone': 'Europe/Stockholm',
            'x-super-properties': self.x_super_properties
        }

    def __call__(self):
        return self.dict

def get_headers():
    typ = config.get("header_type")
    heads = {
        "Windows": WIN_headers,
        "iOS": IOS_headers,
    }

    if typ == "":
        log.info("No Headers Type Selected, Please Choose One")
        make_menu("Window Headers", "IOS Headers")
        head = input(f"  {PINK}[{MAGENTA}Choice{PINK}]{MAGENTA} -> ")
        map = {
            "1": "Windows",
            "2": "iOS"
        }
        if head in map:
            config._set("header_type", map[head])
            typ = map[head]
        else:
            log.failure("Invalid Option")
            sleep(1)
            return get_headers()
    if typ in heads:
        return heads[typ]()()
    else:
        log.failure("Invalid Option")
        sleep(1)
        return get_headers()
    
headers = get_headers()

class Client:
    @staticmethod
    def get_session(token: str = "", cookie: bool = True):
        cv = WIN_headers.chrome_version()
        typ = config.get("header_type")
        iv1, iv2 = str(randint(15,16)), str(randint(1,5))
        idents = {
            "iOS": f"safari_ios_{iv1}_{iv2}",
            "Windows": f"chrome_{cv[:3]}"
        }
        ident = idents.get(typ)
        session = tls_client.Session(
            client_identifier = ident,
            random_tls_extension_order = True
        )
        
        session.headers = headers
        if token != "":
            session.headers.update({"Authorization": token})
        if cookie:
            site = session.get("https://discord.com")
            session.cookies = site.cookies
            
        #session.proxies = {
        #    "http": f"http://3e8j8h0vylsx49g:54nw544u7iglpsm@rp.proxyscrape.com:6060", 
        #    "https": f"http://3e8j8h0vylsx49g:54nw544u7iglpsm@rp.proxyscrape.com:6060"
        #}

        return session