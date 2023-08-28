English video tutorial https://youtu.be/-yjMqXoIejY
Русская видео-инструкция https://www.youtube.com/watch?v=Ezu4LFW_hO8

EraLend Volume Maker

Description
This project aims to automate the process of achieving a desired trading volume on the EraLend platform. It utilizes Python and the Web3 library to interact with the Ethereum blockchain via ZKSync Era.

Requirements
- Python 3.x
- An Ethereum wallet with sufficient liquidity in ETH on ZKSync Era

Setup

1. Download the project.
2. Open a terminal (Command Prompt, PowerShell, Anaconda Prompt, etc.).
3. Navigate to the project directory. For example: 'cd D:/zk_EraLend'
4. Install the required packages: 'pip install -r requirements.txt'

Configuration

1. Edit the config.py file with the following settings:
    gas_treshold: Gas price limit in Gwei. Transactions won't be sent if the current gas price exceeds this limit.
    desired_volume_doll: The desired trading volume in dollars.
    randomize_wallets: Set to True if you want to randomize the order of wallets.
    gas_adjust: Multiplier to adjust the estimated gas limit.
    sleep_time_from: Minimum sleep time between transactions in seconds.
    sleep_time_to: Maximum sleep time between transactions in seconds.

2. Add your private keys to private_keys.txt. Each private key should be on a new line and without quotes.

Run
'python -m main'
