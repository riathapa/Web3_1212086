from web3 import Web3
from Compile import Compile_Solidity
from typing import Tuple
import os



def deploy_contract(contract:str, contract_name:str, account:str, private_key:str, provider:str, chain_id: int): 
    
    compiled_sol = Compile_Solidity(contract)

    #Get the ABI and Byte code
    abi = compiled_sol["contracts"][contract][contract_name]["abi"]
    byte_code = compiled_sol["contracts"][contract][contract_name]["evm"]["bytecode"]["object"]

    connection = Web3(Web3.HTTPProvider(provider))

    contract = connection.eth.contract(abi=abi, bytecode=byte_code)
    nonce = connection.eth.get_transaction_count(account)


    transaction = contract.constructor().build_transaction(
        {
            "chainId":chain_id,
            "gasPrice":connection.eth.gas_price,
            "from":account,
            "nonce":nonce
        }
    )

    signed_txn = connection.eth.account.sign_transaction(transaction, private_key = private_key)

    tx_hash = connection.eth.send_raw_transaction(signed_txn.raw_transaction)

    tx_receipt = connection.eth.wait_for_transaction_receipt(tx_hash)
    return (tx_receipt.contractAddress, abi)



# def main():
#     account = os.getenv("ANVIL_ACCOUNT")
#     private_key = os.getenv("ANVIL_PRIVATE_KEY")
#     provider = os.getenv("LOCAL_PROVIDER")
#     print(provider)
#     # chain_id = os.getenv("ANVIL_CHAIN_ID")
#     contract = "SimpleStorage.sol"
#     # print(account + "\n" + private_key +"\n" + provider + "\n")
#     # print(chain_id)
#     contract_address, abi = deploy_contract(contract, "SimpleStorage", account, private_key, provider, 31337)
#     print(f"Contract deployed at {contract_address}")
#     print(f"ABI: {abi}")
    
# main()
# print(tx_receipt)
# print("Contract deployed at {tx_receipt['contactAddress']}")