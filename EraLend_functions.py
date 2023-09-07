from web3 import Web3
import requests
import json
import random
import os
import time
from loguru import logger

def import_from_file(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f.readlines()]

def get_gas_gwei():
    rpc= 'https://eth.llamarpc.com' 
    web3 = Web3(Web3.HTTPProvider(rpc))
    wei = web3.eth.gas_price
    gwei = web3.from_wei(wei, 'gwei')
    return gwei


def get_eth_price():
    key = "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDC"  
    data = requests.get(key)  
    data = data.json()
    eth_price = float(data['price'])
    return eth_price
    
def get_eth_balance(wallet_address):
    rpc='https://rpc.ankr.com/zksync_era'
    web3 = Web3(Web3.HTTPProvider(rpc))
    return web3.eth.get_balance(Web3.to_checksum_address(wallet_address)) / 10**18


def MakeVolumeEraLend(web3, abi, private_key, desired_volume_doll, gas_treshold, gas_adjust, sleep_time_from, sleep_time_to):
    volume = 0
    retry_time = 3
    account = web3.eth.account.from_key(private_key)
    wallet_address = account.address
    contract_address = '0x22D8b71599e14F20a49a397b88c1C878c86F5579'
    contract = web3.eth.contract(address=contract_address, abi=abi)
    
    logger.debug(f'Wallet {wallet_address} is in process...')
    
    while volume < desired_volume_doll:
        sleep_time = random.randint(sleep_time_from, sleep_time_to)
        current_gas_price = get_gas_gwei()
        if current_gas_price > gas_treshold:
            logger.warning(f"Current gas price {current_gas_price} is above the threshold {gas_treshold}. Skipping transaction.")
            time.sleep(sleep_time)
            continue
        
        logger.info(f"Current volume: {volume}, Desired volume: {desired_volume_doll}")
        eth_balance = get_eth_balance(wallet_address)
        eth_price = get_eth_price()
        doll_balance = eth_price * eth_balance
        amount_minus_remaining_fee = eth_balance - 0.0008
        value_gwei = random.uniform(amount_minus_remaining_fee * 0.997, amount_minus_remaining_fee) 
        value = web3.to_wei(value_gwei, 'ether')
        tx = {
              'from': wallet_address,
              'to': web3.to_checksum_address(contract_address),
              'value': value,
              'nonce': web3.eth.get_transaction_count(wallet_address),
              'maxFeePerGas': web3.eth.gas_price,
              'maxPriorityFeePerGas': web3.eth.gas_price,
              'chainId': 324,
              'data': '0x1249c58b',
              'gas': 0}
        
        
        
        for attempt in range(2):
            tx.update({'nonce': web3.eth.get_transaction_count(wallet_address)})
            gasLimit = round(web3.eth.estimate_gas(tx) * gas_adjust)
            tx.update({'gas': gasLimit})
            try:
                signed_transaction = web3.eth.account.sign_transaction(tx, private_key)
                transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
                receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)
                if receipt['status'] == 1:
                    logger.success(f"Supply tx sent. Hash: {transaction_hash.hex()}")
                    break
                else:
                    logger.error(f"Supply tx failed. Hash: {transaction_hash.hex()}")
                    if attempt == 1:
                        logger.error("Stopping wallet due to consecutive transaction failures.")
                        return
            except Exception as e:
                logger.error(f"An error occurred: {e}")
                if attempt == 1:
                    logger.error("Stopping wallet.")
                    return
                time.sleep(retry_time)
        
        time.sleep(sleep_time)
        
        value = round(contract.functions.balanceOfUnderlying(wallet_address).call() * 0.9999)
        tx = contract.functions.redeemUnderlying(value).build_transaction({
            'from': wallet_address,
            'value': 0,
            'nonce': 0,
            'maxFeePerGas': web3.eth.gas_price,
            'maxPriorityFeePerGas': web3.eth.gas_price,
            'chainId': 324,
            'gas': 0
        })
        
        
        for attempt in range(2):
            tx.update({'nonce': web3.eth.get_transaction_count(wallet_address)})
            gasLimit = round(web3.eth.estimate_gas(tx) * gas_adjust)
            tx.update({'gas': gasLimit})
            try:
                signed_transaction = web3.eth.account.sign_transaction(tx, private_key)
                transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
                receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)
                if receipt['status'] == 1:
                    logger.success(f"Withdraw tx sent. Hash: {transaction_hash.hex()}")
                    break
                else:
                    logger.error(f"Withdraw tx failed. Hash: {transaction_hash.hex()}")
                    if attempt == 1:
                        logger.error("Stopping wallet due to consecutive transaction failures.")
                        return
            except Exception as e:
                logger.error(f"An error occurred: {e}")
                if attempt == 1:
                    logger.error("Stopping wallet.")
                    return
                time.sleep(retry_time)
        
        volume += value_gwei * eth_price
        if volume >= desired_volume_doll:
            logger.success(f'Desired volume: {desired_volume_doll} is achieved for wallet {wallet_address}')
        
        time.sleep(sleep_time)
        
    logger.success('All wallets procedeed')
