from core import *

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("nexus")

class nexus_ui(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        set_title("Main Menu", self)
        self.geometry("800x480")
        self.log = logger(self)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.frame.grid_rowconfigure(4, weight=1)
        self.r = requests.get("https://nexus.vin/assets/img/logo.webp")
        self.image = Image.open(BytesIO(self.r.content))
        with NamedTemporaryFile(delete=False, suffix=".ico") as f: self.image.save(f, format="ICO"); self.icon_path = f.name
        self.wm_iconbitmap(self.icon_path)
        self.image = customtkinter.CTkImage(light_image=self.image, size=(120, 120))
        customtkinter.CTkLabel(self.frame, image=self.image, text="").grid(row=0, column=0, padx=20, pady=10)
        customtkinter.CTkButton(self.frame, text="Main Page", command=lambda: self.switch_tab(0)).grid(row=1, column=0, padx=20, pady=10)
        customtkinter.CTkButton(self.frame, text="Guild Menu", command=lambda: self.switch_tab(1)).grid(row=2, column=0, padx=20, pady=10)
        customtkinter.CTkButton(self.frame, text="Spammers", command=lambda: self.switch_tab(2)).grid(row=3, column=0, padx=20, pady=10)
        customtkinter.CTkButton(self.frame, text="Settings", command=lambda: self.switch_tab(3)).grid(row=6, column=0, padx=20, pady=(10, 10))

        self.tabs_con = customtkinter.CTkFrame(self)
        self.tabs_con.grid(row=0, column=1, rowspan=4, columnspan=3, sticky="nsew")
        self.tabs_con.grid_rowconfigure(0, weight=1)
        self.tabs_con.grid_columnconfigure(0, weight=1)
        self.tabs = []
        for i in range(4):
            tab = customtkinter.CTkFrame(self.tabs_con)
            tab.grid(row=0, column=0, sticky="nsew")
            self.tabs.append(tab)

        self.current_tab = 0
        self.show_tab()

    def switch_tab(self, tab_idx):
        self.current_tab = tab_idx
        self.show_tab()

    def show_tab(self):
        for i, tab in enumerate(self.tabs):
            if i == self.current_tab:
                tab.grid(row=0, column=0, sticky="nsew")
                self.load_tab(i)
                if hasattr(self, 'tabview'):
                    self.tabview.grid() if i == 1 else self.tabview.grid_remove()
                if hasattr(self, 'guildtab'):
                    self.guildtab.grid() if i == 1 else self.guildtab.grid_remove()
                if hasattr(self, 'scrollable_frame'):
                    self.scrollable_frame.grid() if i == 1 else self.scrollable_frame.grid_remove()
            else:
                tab.grid_remove()

    def load_tab(self, tab_idx):
        for tab in self.tabs:
            for widget in tab.winfo_children():
                widget.destroy()

        map = {
            0: self.main_menu,
            1: self.joiner_menu,
            2: self.spammer_menu,
            3: self.config_menu
        }

        if tab_idx in map:
            map[tab_idx]()

    def main_menu(self):
        label = customtkinter.CTkLabel(self.tabs[0], text="Main Page")
        set_title("Main Manu", self)
        label.pack()

        button = customtkinter.CTkButton(self.tabs[0], text="Click Me", command=self.button_clicked)
        button.pack()

    def button_clicked(self):
        self.log.info("Button clicked!")

    def joiner_menu(self):
        set_title("Guild Menu", self)
        self.guildtab = customtkinter.CTkTabview(self, width=250, bg_color="#333333", corner_radius=10)
        self.guildtab.grid(row=0, column=1)
        for tab in ["Joiner", "Leaver"]:
            self.guildtab.add(tab)
            self.guildtab.tab(tab).grid_columnconfigure(0, weight=1)

        self.invite = customtkinter.CTkEntry(self.guildtab.tab("Joiner"), width=170, placeholder_text="Invite")
        self.guild_id = customtkinter.CTkEntry(self.guildtab.tab("Joiner"), width=170, placeholder_text="Guild ID")
        self.bot_message = customtkinter.CTkEntry(self.guildtab.tab("Joiner"), width=170, placeholder_text="Message Link / Bot ID")

        self.invite.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.guild_id.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.bot_message.grid(row=3, column=0, padx=20, pady=(10, 10))

        self.leaver_guild_id = customtkinter.CTkEntry(self.guildtab.tab("Leaver"), width=170, placeholder_text="Guild ID")
        self.leaver_guild_id.grid(row=1, column=0, padx=20, pady=(10, 10))

        def leaver_run():
            guild_id = self.leaver_guild_id.get()
            if guild_id != '': threading.Thread(target=token_leaver, args=[self, guild_id]).start()
            else: self.log.failure("Guild ID box is empty!")

        customtkinter.CTkButton(self.guildtab.tab("Leaver"), text="Leave", command=leaver_run).grid(row=2, column=0, padx=20, pady=20)

        def run():
            vars = {
                'link': (self.invite.get(), "Link is empty!"),
                'guild_id': (self.guild_id.get(), "Guild ID is empty!"),
                'bot_message': (self.bot_message.get(), "Message link box is empty!", "Bot ID box is empty!")
            }

            if not any(switch.get() for switch in self.switches):
                self.log.failure("No switch is enabled!")
                return

            actions = {
                0: lambda: threading.Thread(target=token_joiner, args=[self, vars['link'][0]]).start() 
                    if vars['link'][0] != '' 
                    else self.log.failure(vars['link'][1]),

                1: lambda: threading.Thread(target=wick_captcha, args=[self, vars['bot_message'][0]]).start() 
                    if vars['bot_message'][0] != '' 
                    else self.log.failure(vars['bot_message'][1]),

                2: lambda: threading.Thread(target=restorecord_bypass, args=[self, vars['guild_id'][0], vars['bot_message'][0]]).start() 
                    if vars['guild_id'][0] != '' and vars['bot_message'][0] != '' 
                    else self.log.failure(vars['guild_id'][1] if vars['guild_id'][0] == '' else vars['bot_message'][2]),

                3: lambda: threading.Thread(target=sledge_hammer, args=[self, vars['bot_message'][0]]).start() 
                    if vars['bot_message'][0] != '' 
                    else self.log.failure(vars['bot_message'][1]),

                4: lambda: threading.Thread(target=bypass_rules, args=[self, vars['guild_id'][0]]).start() 
                    if vars['guild_id'][0] != '' 
                    else self.log.failure(vars['guild_id'][1])
            }
            for i, switch in enumerate(self.switches):
                if switch.get():
                    actions.get(i)()

        customtkinter.CTkButton(self.guildtab.tab("Joiner"), text="Run", command=run).grid(row=4, column=0, padx=20, pady=20)

        self.scroll = customtkinter.CTkScrollableFrame(self, bg_color="#333333", label_text="Options", corner_radius=12)
        self.scroll.grid(row=0, column=2, padx=45)
        self.scroll.grid_columnconfigure(0, weight=1)

        options = ["Join Guild", "Restorecord", "Sledge Hammer", "Rules Bypass", "Wick Captcha"]
        self.switches = []

        for i, option in enumerate(options):
            if option == "Join Guild": 
                switch = customtkinter.CTkCheckBox(master=self.scroll, text=option)
                switch.select()
            else: 
                switch = customtkinter.CTkCheckBox(master=self.scroll, text=option)
            switch.grid(row=i, column=0, padx=10, pady=(0, 20), sticky='w')
            self.switches.append(switch)
        self.console = customtkinter.CTkTextbox(self.tabs[1], width=560, height=150)
        self.console.grid(row=2, column=1, padx=20, pady=318)

    def spammer_menu(self):
        label = customtkinter.CTkLabel(self.tabs[2], text="Main Page")
        set_title("Main Manu", self)
        label.pack()

        button = customtkinter.CTkButton(self.tabs[2], text="Click Me", command=self.button_clicked)
        button.pack()

    def config_menu(self):
        set_title("Config Menu", self)
        data = json.load(open('config.json'))
        self.entries = {}

        for i, (k, v) in enumerate(data.items(), start=1):
            customtkinter.CTkLabel(self.tabs[3], text=k.replace('_', ' '), font=("Helvetica", 12, "bold")).grid(row=i, column=0, sticky='nsew', padx=10, pady=10)
            widget = self.create_widget(k, v)
            widget.grid(row=i, column=1, sticky='nsew', padx=10, pady=10)
            self.entries[k] = widget

        customtkinter.CTkButton(self.tabs[3], text="Save", command=self.save_config).grid(row=i+1, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)

    def create_widget(self, key, value):
        if isinstance(value, bool):
            return customtkinter.CTkCheckBox(self.tabs[3], variable=tk.IntVar(value=value), text="")
        if key == 'header_type':
            return customtkinter.CTkOptionMenu(self.tabs[3], variable=tk.StringVar(value=value), values=["iOS", "Windows"])
        if key == 'captcha_type':
            return customtkinter.CTkOptionMenu(self.tabs[3], variable=tk.StringVar(value=value), values=["Nexcha", "Hcopcha", "Capsolver"])
        widget = customtkinter.CTkEntry(self.tabs[3], font=("Helvetica", 12, "bold"))
        widget.insert(0, str(value))
        return widget
 
    def save_config(self):
        content = {key: (lambda e: bool(int(e.get())) if isinstance(e, customtkinter.CTkCheckBox) else e.get())(entry) for key, entry in self.entries.items()}
        with open('config.json', 'w') as f:
            json.dump(content, f, indent=4)
            self.log.info("New config successfully saved!")

if __name__ == "__main__":
    g = nexus_ui()
    g.mainloop()