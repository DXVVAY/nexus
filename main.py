from core import *

class ui:
 
    def __init__(self):
        self.menu_ops = {
            '1': ('Token Joiner', token_joiner),
            '2': ('Token Leaver', token_leaver),
            '3': ('Channel Spammer', token_spammer),
            '4': ('Checker Menu', self.tempfunc),
            '5': ('Bypass Rules', self.tempfunc),
            '6': ('Restorecord Bypass', self.tempfunc),
            '7': ('Sledge Hammer', self.tempfunc),
            '8': ('Button Presser', self.tempfunc),
            '9': ('Token Reactor', self.tempfunc),
            '10': ('Global Nicker', self.tempfunc),
            '11': ('Server Nicker', self.tempfunc),
            '12': ('Hypesquad Changer', self.tempfunc),
            '13': ('Token Bio Changer', bio_changer),
            '14': ('Token Pron Changer', pron_changer),
            '15': ('VC Menu', self.tempfunc),
            '16': ('Soundboard Spam', self.tempfunc),
            '17': ('Token Typer', self.tempfunc),
            '18': ('Forum Spammer', self.tempfunc),
            '19': ('User Mass Friend', self.tempfunc),
            '20': ('User Mass DM', self.tempfunc),
            '21': ('Server Mass Friend', self.tempfunc),
            '22': ('Mass Report', self.tempfunc),
            '23': ('Mass Thread', self.tempfunc),
            '24': ('Server booster', self.tempfunc),
        }
        self.WHITE = "\u001b[37m"
        self.PINK = "\033[38;5;176m"
        self.MAGENTA = "\033[38;5;97m"
        self.START_COLOR = [111, 70, 130]
        self.END_COLOR = [218, 112, 214]

        self.ASCII = f"""



                                   ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
                                   ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝ {self.PINK}[{self.MAGENTA}Website{self.PINK}] {self.WHITE}| Nexus.vin
                                   ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗ {self.PINK}[{self.MAGENTA}Tokens{self.PINK}]  {self.WHITE}| {len(config.get_tokens())}
                                   ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║ {self.PINK}[{self.MAGENTA}Client{self.PINK}]  {self.WHITE}| {utility.get_client_type()}
                                   ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║ {self.PINK}[{self.MAGENTA}Discord{self.PINK}] {self.WHITE}| nexustool
                                   ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
        """
        
    def make_menu(self):
        str = ""
        keys = list(self.menu_ops.keys())
        for i in range(6):
            for j in range(i, len(self.menu_ops), 6):
                key = keys[j]
                label, _ = self.menu_ops[key]
                str += f"  {self.PINK}[{self.MAGENTA}{key.zfill(2)}{self.PINK}] {self.WHITE}| {label.ljust(21)}"
            str += "\n"
        return str

    def main_screen(self):
        try:
            if not locals()["_"].success:
                return
        except:
            return

        set_title("Main Menu")
        while True:
            utility.clear()
            print(Center.XCenter(vgratient(self.ASCII, self.START_COLOR, self.END_COLOR)))
            print(Center.XCenter(self.make_menu()))

            while True:
                print()
                ch = input(f"  {self.PINK}[{self.MAGENTA}Choice{self.PINK}]{self.MAGENTA} -> ").lstrip("0")
                cc = ch.upper()
                if cc in self.menu_ops:
                    choice = cc
                    break
                else:
                    log.warning("Invalid option. Please try again.")
                    sleep(1)
                    self.main_screen()

            _, func = self.menu_ops[choice]
            func()

    def tempfunc(self):
        print("temp func")
        log.PETC()
        self.main_screen()

def main():
    try:
        locals()["_"]=Auth().authenticate()
        ui().main_screen()
    except Exception as e:
        log.failure(e)
        log.PETC()
        main()

if __name__ == "__main__":
    main()
