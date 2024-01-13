class logger:
    WHITE = "\u001b[37m"
    MAGENTA = "\033[38;5;97m"
    RED = "\u001b[31m"
    GREEN = "\u001b[32m"
    YELLOW = "\u001b[33m";
    BLUE = "\u001b[34m";
    PINK = "\033[38;5;176m"

    def success(Message):
        print(f"{logger.PINK}[{logger.MAGENTA}Nexus{logger.PINK}]{logger.WHITE} | {logger.PINK}[{logger.GREEN}Success{logger.PINK}] {logger.WHITE}| {logger.PINK}[{logger.MAGENTA}{Message}{logger.PINK}]")

    def warning(Message):
        print(f"{logger.PINK}[{logger.MAGENTA}Nexus{logger.PINK}]{logger.WHITE} | {logger.PINK}[{logger.YELLOW}Warning{logger.PINK}] {logger.WHITE}| {logger.PINK}[{logger.MAGENTA}{Message}{logger.PINK}]")

    def welcome(Message):
        print(f"{logger.PINK}[{logger.MAGENTA}Nexus{logger.PINK}]{logger.WHITE} | {logger.PINK}[{logger.BLUE}Welcome{logger.PINK}] {logger.WHITE}| {logger.PINK}[{logger.MAGENTA}{Message}{logger.PINK}]")

    def failure(Message):
        print(f"{logger.PINK}[{logger.MAGENTA}Nexus{logger.PINK}]{logger.WHITE} | {logger.PINK}[{logger.RED}Failure{logger.PINK}] {logger.WHITE}| {logger.PINK}[{logger.MAGENTA}{Message}{logger.PINK}]")