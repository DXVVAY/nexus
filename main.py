from core import *

class ui:
    WHITE = "\u001b[37m"
    PINK = "\033[38;5;176m"
    MAGENTA = "\033[38;5;97m"
    PINK = "\033[38;5;176m"
    START_COLOR = [111, 70, 130]
    END_COLOR = [218, 112, 214]

    ASCII = f"""



                                  ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
                                  ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝ {PINK}[{MAGENTA}Website{PINK}] {WHITE}| Nexus.vin
                                  ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗ {PINK}[{MAGENTA}Tokens{PINK}]  {WHITE}| {len(config.get_tokens())}
                                  ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║ {PINK}[{MAGENTA}Client{PINK}]  {WHITE}| {utility.get_client_type()}
                                  ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║ {PINK}[{MAGENTA}Discord{PINK}] {WHITE}| nexustool
                                  ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
    """
    MENU = f"""
      {PINK}[{MAGENTA}01{PINK}] {WHITE}| Joiner Menu         {PINK}[{MAGENTA}07{PINK}] {WHITE}| Sledge Hammer       {PINK}[{MAGENTA}13{PINK}] {WHITE}| Token Bio Changer   {PINK}[{MAGENTA}19{PINK}] {WHITE}| User Mass Friend
      {PINK}[{MAGENTA}02{PINK}] {WHITE}| Token Leaver        {PINK}[{MAGENTA}08{PINK}] {WHITE}| Button Presser      {PINK}[{MAGENTA}14{PINK}] {WHITE}| Token Pron Changer  {PINK}[{MAGENTA}20{PINK}] {WHITE}| User Mass DM
      {PINK}[{MAGENTA}03{PINK}] {WHITE}| Channel Spammer     {PINK}[{MAGENTA}09{PINK}] {WHITE}| Token Reactor       {PINK}[{MAGENTA}15{PINK}] {WHITE}| VC Menu             {PINK}[{MAGENTA}21{PINK}] {WHITE}| Server Mass Friend
      {PINK}[{MAGENTA}04{PINK}] {WHITE}| Checker Menu        {PINK}[{MAGENTA}10{PINK}] {WHITE}| Global Nicker       {PINK}[{MAGENTA}16{PINK}] {WHITE}| Soundboard Spammer  {PINK}[{MAGENTA}22{PINK}] {WHITE}| Mass Report
      {PINK}[{MAGENTA}05{PINK}] {WHITE}| Bypass Rules        {PINK}[{MAGENTA}11{PINK}] {WHITE}| Server Nicker       {PINK}[{MAGENTA}17{PINK}] {WHITE}| Token Typer         {PINK}[{MAGENTA}23{PINK}] {WHITE}| Mass Thread
      {PINK}[{MAGENTA}06{PINK}] {WHITE}| Restorecord Bypass  {PINK}[{MAGENTA}12{PINK}] {WHITE}| Hypesquad Changer   {PINK}[{MAGENTA}18{PINK}] {WHITE}| Forum Spammer       {PINK}[{MAGENTA}24{PINK}] {WHITE}| Webhook Tool
    """

    def __init__(self):
        self.menu_options = {
            '1': ('Joiner Menu', self.tempfunc),
            '2': ('Token Leaver', self.tempfunc),
            '3': ('Channel Spammer', self.tempfunc),
            '4': ('Checker Menu', self.tempfunc),
            '5': ('Bypass Rules', self.tempfunc),
            '6': ('Restorecord Bypass', self.tempfunc),
            '7': ('Sledge Hammer', self.tempfunc),
            '8': ('Button Presser', self.tempfunc),
            '9': ('Token Reactor', self.tempfunc),
            '10': ('Global Nicker', self.tempfunc),
            '11': ('Server Nicker', self.tempfunc),
            '12': ('Hypesquad Changer', self.tempfunc),
            '13': ('Token Bio Changer', self.tempfunc),
            '14': ('Token Pron Changer', self.tempfunc),
            '15': ('VC Menu', self.tempfunc),
            '16': ('Soundboard Spammer', self.tempfunc),
            '17': ('Token Typer', self.tempfunc),
            '18': ('Forum Spammer', self.tempfunc),
            '19': ('User Mass Friend', self.tempfunc),
            '20': ('User Mass DM', self.tempfunc),
            '21': ('Server Mass Friend', self.tempfunc),
            '22': ('Mass Report', self.tempfunc),
            '23': ('Mass Thread', self.tempfunc),
            '24': ('Webhook Tool', self.tempfunc),
        }

    def main_screen(self):
        while True:
            utility.clear()
            print(Center.XCenter(vgratient(self.ASCII, self.START_COLOR, self.END_COLOR)))
            print(Center.XCenter(self.MENU))
            while True:
                cc = input(f"      {self.PINK}[{self.MAGENTA}Choice{self.PINK}]{self.MAGENTA} -> ")
                if cc in self.menu_options:
                    choice = cc
                    break
                else:
                    log.warning("Invalid option. Please try again.")
                    sleep(1)
                    self.main_screen()

            _, func = self.menu_options[choice]
            func()

    def tempfunc(self):
        print("temp func")
        log.PETC()
        self.main_screen()

def main():
    try:
        Auth.authenticate()
        ui().main_screen()
    except Exception as e:
        log.failure(e)
        log.PETC()
        main()

if __name__ == "__main__":
    main()
