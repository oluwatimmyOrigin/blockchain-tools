from web3 import Web3
from eth_account import Account
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import time

# Connect to a Web3 provider, such as Infura or Alchemy
web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/<YOUR-PROJECT-ID>'))

# Set your private key for the account that initiates the swap
private_key = 'your_private_key_here'

# Specify the Uniswap Router address
uniswap_router_address = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'  # Replace with the actual address

# Specify the token you want to swap to
token_to_swap_address = '0x6B175474E89094C44Da98b954EedeAC495271d0F'  # Replace with the actual address

# Enable unaudited HD wallet features
Account.enable_unaudited_hdwallet_features()

# Set the seed phrase
seed_phrase = 'your seed phrase here'

def generate_eth_address(seed_phrase, index):
    account = web3.eth.account.from_mnemonic(seed_phrase, f"m/44'/60'/0'/0/{index}")
    return account.address

def initiate_swap(user_eth_address, token_to_swap_address, eth_amount_to_swap):
    # Construct the transaction to swap ETH for tokens
    transaction = {
        'to': uniswap_router_address,
        'value': eth_amount_to_swap,
        'gas': 200000,  # Replace with an appropriate gas limit
        'gasPrice': web3.toWei('50', 'gwei'),  # Replace with an appropriate gas price
        'nonce': web3.eth.getTransactionCount(user_eth_address),
        'data': web3.uniswap.encode_input('swapExactETHForTokens', [0, [web3.eth.WETH.address, token_to_swap_address], user_eth_address, 9999999999]),
    }

    # Sign the transaction
    signed_transaction = web3.eth.account.signTransaction(transaction, private_key)

    # Send the transaction
    transaction_hash = web3.eth.sendRawTransaction(signed_transaction.rawTransaction)

    return transaction_hash

def check_swap_status(transaction_hash):
    # Wait for the transaction to be mined
    receipt = None
    while receipt is None:
        try:
            receipt = web3.eth.getTransactionReceipt(transaction_hash)
        except web3.exceptions.TransactionNotFound:
            time.sleep(5)  # Wait for 5 seconds if the transaction is not found

    # Extract relevant information from the receipt
    success = receipt['status'] == 1
    return success

def send_tokens_back(user_eth_address, token_to_swap_address, swapped_token_amount):
    # Assume there's a function on the token contract for transferring tokens
    # Replace 'transfer' with the actual function name if necessary
    token_contract = web3.eth.contract(address=token_to_swap_address, abi=your_token_abi_here)
    transaction = token_contract.functions.transfer(user_eth_address, swapped_token_amount).buildTransaction({
        'gas': 100000,  # Replace with an appropriate gas limit
        'gasPrice': web3.toWei('50', 'gwei'),  # Replace with an appropriate gas price
        'nonce': web3.eth.getTransactionCount(web3.eth.accounts[0]),  # Use the sender's address nonce
    })

    # Sign and send the transaction
    signed_transaction = web3.eth.account.signTransaction(transaction, private_key)
    transaction_hash = web3.eth.sendRawTransaction(signed_transaction.rawTransaction)

    return transaction_hash

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome! Use /swap to initiate a swap.')

def swap(update: Update, context: CallbackContext) -> None:
    # Example usage
    user_eth_address = generate_eth_address(seed_phrase, 0)  # Generate ETH address for the user
    eth_amount_to_swap = web3.toWei(1, 'ether')  # 1 ETH for example

    # Initiate the swap
    swap_transaction_hash = initiate_swap(user_eth_address, token_to_swap_address, eth_amount_to_swap)

    # Check the status of the swap
    swap_success = check_swap_status(swap_transaction_hash)

    if swap_success:
        update.message.reply_text("Swap successful!")

        # Example: Send swapped tokens back to the user
        swapped_token_amount = web3.toWei(500, 'ether')  # Replace with the actual amount of tokens to send back
        send_tokens_back(user_eth_address, token_to_swap_address, swapped_token_amount)
        update.message.reply_text("Tokens sent back to the user.")
    else:
        update.message.reply_text("Swap failed.")

def main():
    # Set your Telegram bot token
    updater = Updater(token='your_bot_token_here', use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("swap", swap))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop it
    updater.idle()

if __name__ == '__main__':
    main()
