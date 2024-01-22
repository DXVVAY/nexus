# Nexus Core!!!

# all imports needed
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
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
import hashlib
import base64
import random
import httpx
import string
import shutil
import ctypes
import types
import json
import time
import uuid
import hmac
import jwt
import sys
import os
import re

def clear():
    system = os.name
    if system == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    return
clear()

from .plugs.logger import *
from .plugs.config import *

def set_title(text: str):
    system = os.name
    title = f"[Nexus] | [{text}] | [Tokens: {len(config.get_tokens())}] | [Nexus.vin]"
    if system == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    elif system == 'posix':
        sys.stdout.write(title)
    #TODO: make a discord rpc later

from .plugs.auth import *
from .plugs.utils import*
from .plugs.headers import *
from .plugs.scraper import *

# functions
from .funcs.token_joiner import *
from .funcs.token_leaver import *
from .funcs.token_spammer import *
from .funcs.bio_changer import *