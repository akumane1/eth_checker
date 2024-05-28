import requests
import time
from eth_account import Account
from mnemonic import Mnemonic
from colorama import Fore, Style, init

# Initialize colorama
init()

# Enable the unaudited HD wallet features
Account.enable_unaudited_hdwallet_features()

# Your Etherscan API key (replace 'YourApiKeyToken' with your actual API key)
ETHERSCAN_API_KEY = 'VFM8F4Y2TZAXGD8Q3621TKT1P33J54VT3V'
ETHERSCAN_API_URL = 'https://api.etherscan.io/api'

# Function to get the balance of an Ethereum address
def get_eth_balance(address):
    params = {
        'module': 'account',
        'action': 'balance',
        'address': address,
        'tag': 'latest',
        'apikey': ETHERSCAN_API_KEY
    }
    response = requests.get(ETHERSCAN_API_URL, params=params)
    data = response.json()
    if data['status'] == '1':
        balance_wei = int(data['result'])
        balance_eth = balance_wei / 10**18
        return balance_eth
    else:
        return None

# Infinite loop to generate seed phrases and check balances
while True:
    # Generate a mnemonic seed phrase
    mnemo = Mnemonic("english")
    seed_phrase = mnemo.generate(strength=128)  # 12-word seed phrase

    # Derive private key and address from the seed phrase using standard Ethereum derivation path (m/44'/60'/0'/0/0)
    account = Account.from_mnemonic(seed_phrase)
    private_key = account.key.hex()
    address = account.address

    # Display the seed phrase, private key, and address
    print(f"Seed Phrase: {Fore.YELLOW}{seed_phrase}{Style.RESET_ALL}")
    print(f"Private Key: {Fore.CYAN}{private_key}{Style.RESET_ALL}")
    print(f"Address: {Fore.CYAN}{address}{Style.RESET_ALL}")

    # Check the balance of the generated address
    balance = get_eth_balance(address)
    if balance is not None:
        print(f"Balance: {Fore.RED}{balance} ETH\n" + Style.RESET_ALL)
        if balance > 0.0:
            print(Fore.GREEN + "WOOHOO!! \nThe balance is greater than 0.0 ETH!" + Style.RESET_ALL)
            break
    else:
        print("Error fetching balance. Please check the address or API key.")
    
    # Wait for a short interval before generating the next seed phrase and checking the balance
    time.sleep(0.01)
