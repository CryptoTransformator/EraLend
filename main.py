from EraLend_functions import *
from config import *
from web3 import Web3
import requests
import json
import random
import os
from loguru import logger

current_working_directory = os.getcwd()
web3 = Web3(Web3.HTTPProvider('https://rpc.ankr.com/zksync_era'))

with open(os.path.join(current_working_directory, 'abi.json'), 'r') as file:
    abi = json.load(file)
    
private_keys = import_from_file(os.path.join(current_working_directory, 'private_keys.txt'))
if randomize_wallets:
    random.seed(32)
    random.shuffle(private_keys)


logger.success(f'Created by CryptoTransformator')
logger.info(f'https://github.com/CryptoTransformator')
logger.info(f'https://t.me/gori_levi')

for private_key in private_keys:
    MakeVolumeEraLend(web3, abi, private_key, desired_volume_doll, gas_treshold, gas_adjust, sleep_time_from, sleep_time_to)
















