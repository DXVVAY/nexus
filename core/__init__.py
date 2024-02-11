# Nexus Core!!!

__title__ = 'Nexus'
__author__ = 'DEXV', "Cyprian"
__copyright__ = 'Copyright 2022-present nexus'
__version__ = '1.0.0'

# all 3rd party imports needed
from datetime import datetime, timedelta, timezone
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Optional, Union
from tkinter.filedialog import askopenfilename
from base64 import b64encode
from decimal import Decimal
from random import randint
from pystyle import Center
from colorama import Fore
from ab5 import vgratient
from time import sleep
import tls_client
import websocket
import threading
import platform
import requests
import keyboard
import delorean
import base64
import random
import string
import shutil
import ctypes
import types
import httpx
import json
import time
import uuid
import hmac
import jwt
import sys
import os
import re

def clear() -> None:
    system = os.name
    if system == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    return
clear()

# Mandetory imports
from .plugs.logger import *
from .plugs.config import *

def set_title(text: str) -> None:
    system = os.name
    title = f"[Nexus]  |  [{text}]  |  [Tokens: {len(config.get_tokens())}]  |  [Nexus.vin]"
    if system == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    elif system == 'posix':
        sys.stdout.write(title)
    # TODO: make a discord rpc later

from .plugs.websocket import *
from .plugs.utils import*
from .plugs.headers import *
from .plugs.scraper import *

# solvers
from .solvers import *

# functions
from .funcs.token_joiner import *
from .funcs.token_leaver import *
from .funcs.token_spammer import *
from .funcs.bio_changer import *
from .funcs.pron_changer import *
from .funcs.guild_checker import *
from .funcs.token_checker import *
from .funcs.server_booster import *
from .funcs.button_presser import *
from .funcs.message_reactor import *
from .funcs.pfp_changer import *
from .funcs.server_mass_friend import *
from .funcs.nicker import *

# bypasses
from .bypass.sledge_hammer import *
from .bypass.guild_rules import *
from .bypass.wick_captcha import *
from .bypass.restore_cord import *