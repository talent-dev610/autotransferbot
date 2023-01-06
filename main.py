import threading
from tracemalloc import stop
from web3 import Web3
from tronpy import Tron
w3_bnb = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org"))
w3_eth = Web3(Web3.HTTPProvider("https://eth.llamarpc.com"))
w3_trx = Web3(Web3.HTTPProvider("https://api.trongrid.io/jsonrpc"))
private_key = "a1c9df6332c6884853c148a300cf2f743692e03d47499766a65ccf763a96b830"
pub_key ="0x8e2D8b7E3933c483C4bB1c90a02385575ECF14d4"

recipient_pub_key = "0x97123ebfA7e51cAb93a50D376cC3546966445447"
ACCOUNTADDRESS = Web3.toChecksumAddress(pub_key)

def send_eth(amount, provider):
    # get the nonce.  Prevents one from sending the transaction twice
    nonce = provider.eth.getTransactionCount(ACCOUNTADDRESS)
    gasPrice = provider.eth.gas_price
    gas = 21000
    gasFee = gasPrice * gas
    print(gasFee)
    if gasFee > amount:
        return
    # build a transaction in a dictionary
    tx = {
        'nonce': nonce,
        'to': recipient_pub_key,
        'value': amount-gasFee,
        'gas': 21000,
        'gasPrice': gasPrice
    }

    # sign the transaction
    signed_tx = provider.eth.account.sign_transaction(tx, private_key)

    # send transaction
    tx_hash = provider.eth.sendRawTransaction(signed_tx.rawTransaction)

    # get transaction hash
    print(provider.toHex(tx_hash))

def bsc_bot():
    while True:
        balance_bnb = w3_bnb.eth.get_balance(pub_key)
        print()
        print(balance_bnb)
        balance_eth = w3_eth.eth.get_balance(pub_key)
        print(balance_eth)
        balance_trx = w3_trx.eth.get_balance(pub_key)
        try:
            if balance_bnb > 0:
                send_eth(balance_bnb, w3_bnb)
        except:
            print("insufficient funds")

def eth_bot():
    while True:
        balance_eth = w3_eth.eth.get_balance(pub_key)
        print(balance_eth)
        try:
            if balance_eth > 0:
                send_eth(balance_eth, w3_eth)
        except:
            print("insufficient funds")

print("start")
if __name__ == '__main__':
    threading.Thread(target=bsc_bot).start()
    threading.Thread(target=eth_bot).start()
input('Press Enter to exit.')