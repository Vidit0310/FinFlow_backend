import json
from web3 import Web3

def register_user(name, birthdate, pan, ufid):
    """
    Registers a user on the Ethereum blockchain.

    Parameters:
    - name (str): User's name.
    - birthdate (str): User's birthdate (YYYY-MM-DD).
    - pan (str): User's PAN number.
    - ufid (str): Unique Financial ID.
    """
    
    # ✅ Connect to Ethereum network (Infura/Local Node)
    infura_url = "https://sepolia.infura.io/v3/b7311a67bf3241699ec2664cea529bef"  # Replace with your Infura ID
    web3 = Web3(Web3.HTTPProvider(infura_url))

    if not web3.is_connected():
        print("❌ Connection Failed")
        return

    print("✅ Connected to Ethereum Blockchain")

    # ✅ Deployed contract details
    contract_address = "0x338284B178de240bd7F95290cd8e9ae33c7419E5"  # Replace with your contract address

    # Load contract ABI
    with open("contract.json", "r") as file:
        contract_abi = json.load(file)  

    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    # ✅ User details
    user_address = "0xD80597EfB69d64af2E6B55be48143ee9BfEDcCE9"  # Sender's address
    private_key = "8acc00365772ea71de61eac366c0d1b0acec06d4b50ec623b82b2a672ce2d674"  # ⚠️ Never expose in production!

    # ✅ Build transaction
    txn = contract.functions.registerUser(name, birthdate, pan, ufid).build_transaction({
        'from': user_address,
        'gas': 200000,
        'gasPrice': web3.to_wei('5', 'gwei'),
        'nonce': web3.eth.get_transaction_count(user_address),
    })

    # ✅ Sign transaction
    signed_txn = web3.eth.account.sign_transaction(txn, private_key)

    # ✅ Send transaction
    txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

    # ✅ Wait for transaction receipt
    txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)

    print(f"✅ Transaction successful! Hash: {txn_hash.hex()}")
    return txn_hash.hex()


