from core import *

class ui:
    def __init__(self):
        self.menu_ops = {
            '1': ('Token Joiner', token_joiner),
            '2': ('Token Leaver', token_leaver),
            '3': ('Channel Spammer', token_spammer),
            '4': ('Checker Menu', self.checker_menu),
            '5': ('Bypass Menu', self.bypass_menu),
            '6': ('Voice Chat Menu', self.tempfunc),
            '7': ('Avatar Changer', pfp_changer),
            '8': ('Token Humanizer', self.tempfunc),
            '9': ('Token Nicker', Nick_changer),
            '10': ('Hypesquad Changer', self.tempfunc),
            '11': ('Token Bio Changer', self.tempfunc),
            '12': ('Pronouns Changer', pron_changer),
            '13': ('Soundboard Spammer', server_booster),
            '14': ('Server Booster', self.tempfunc),
            '15': ('Forum Spammer', self.tempfunc),
            '16': ('Call Spammer', self.tempfunc),
            '17': ('Mass Thread', self.tempfunc),
            '18': ('Mass Report', self.tempfunc),
            '19': ('User Mass Friend', self.tempfunc),
            '20': ('User Mass DM', self.tempfunc),
            '21': ('Server Mass Friend', user_mass_friend),
            '22': ('Server Mass DM', self.tempfunc),
            '23': ('Button Presser', button_presser),
            '24': ('Message Reactor', message_reactor),
        }
        self.WHITE = "\u001b[37m"
        self.PINK = "\033[38;5;176m"
        self.MAGENTA = "\033[38;5;97m"
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
        for i in range(6):
            for j in range(i, len(self.menu_ops), 6):
                key = list(self.menu_ops.keys())[j]
                label, _ = self.menu_ops[key]
                str += f"    {self.PINK}[{self.MAGENTA}{key.zfill(2)}{self.PINK}] {self.WHITE}| {label.ljust(18)}"
            str += "\n"
        return str

    def main_screen(self):
        set_title("Main Menu")
        while True:
            utility.clear()
            print(Center.XCenter(vgratient(self.ASCII, [111, 70, 130], [218, 112, 214])))
            print(self.make_menu())

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
    
    def checker_menu(self):
        set_title("Checker Menu")
        utility.make_menu("Token Checker", "Guild Checker")
        choice = utility.ask("Choice")
        chs = {"1": token_checker, "2": server_checker}
        if choice in chs:
            chs[choice]()
        else:
            log.warning("Invalid option. Please try again.")
            sleep(1)
            self.main_screen()

    def bypass_menu(self):
        set_title("Checker Menu")
        utility.make_menu("Restorecord", "Sledge Hammer", "Rules Bypass", "Wick Captcha")
        choice = utility.ask("Choice")
        chs = {"1": restorecord_bypass, "2": sledge_hammer, "3": bypass_rules, "4": wick_captcha}
        if choice in chs:
            chs[choice]()
        else:
            log.warning("Invalid option. Please try again.")
            sleep(1)
            self.main_screen()

def main():
    try:
        Auth().authenticate()
        ui().main_screen()
    except Exception as e:
        log.failure(e)
        log.PETC()
        main()

if __name__ == "__main__":
    main()
