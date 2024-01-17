# Nexus Core!!!

# all imports needed
from datetime import datetime
from colorama import Fore
from random import randint
from time import sleep
import tls_client
import websocket
import platform
import requests
import hashlib
import base64
import random
import httpx
import signal
import json
import uuid
import hmac
import jwt
import sys
import os
import re

# initially clear the console on start
import os
def clear():
    system = os.name
    if system == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    return
clear()

# plugs
from .plugs.logger import *
from .plugs.config import *
from .plugs.auth import *
from .plugs.utils import*
from .plugs.headers import *
from .plugs.scraper import *
