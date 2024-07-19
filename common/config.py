import os
from backports import configparser

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join(".ini")))