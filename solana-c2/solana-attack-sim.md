# Solana C2 Test

***

## Summary
I am starting to see a trend in malware where some are using Solana Blockchain as a C2 to send commands to their implants. Instances like Glassworm and Windsurf are the recent ones. I want to create a benign test to see how it works and what possible detections to look for.

## What is a blockchain?
At its core, a blockchain is a decentralized, digital ledger that records transactions across many computers. Think of it as a shared Excel spreadsheet where everyone has a copy, but no single person can edit old entries.

What are some key characteristics?
1. Decentralization: No central authority (like a bank) controls the data.
2. Immutability: Once a "block" of data is added to the "chain," it is nearly impossible to change without altering every subsequent block.
3. Transparency: In public blockchains, anyone can view the transaction history.
4. Consensus: The network uses specific rules (like Proof of Work or Proof of Stake) to agree that a transaction is valid before adding it.

## What is Solana blockchain?
Solana is a high-performance public blockchain designed for widespread adoption by being significantly faster and cheaper than older networks like Ethereum or Bitcoin. It is often referred to as a "World Computer" because it supports Smart Contracts, which are self-executing code that powers decentralized apps (dApps), NFTs, and decentralized finance (DeFi).

Key characteristics include:
1. Proof of History (PoH): This is Solana's secret sauce. Instead of nodes having to talk to each other to agree on what time a transaction happened, PoH creates a historical record that proves an event occurred at a specific moment in time. This acts like a digital clock for the network.
2. High Throughput: Because of PoH and other optimizations, Solana can theoretically handle over 50,000 transactions per second (TPS), whereas Ethereum often handles fewer than 30.
3. Low Cost: Transaction fees on Solana are typically a fraction of a cent ($0.00025$), making it ideal for microtransactions and gaming.

## How is it used maliciously?
Here's how the Glassworm malware works:
1. The attacker sends a micro-transaction (a tiny amount of SOL, which is Solana's currency) to their own controlled wallet.
2. Solana allows users to attach a "Memo" (a string of text) to any transaction. The attacker places a Base64-encoded URL into this memo field.
3. When Glassworm infects a machine, it uses public Solana RPC nodes (like api.mainnet-beta.solana.com) to query the transaction history of that specific wallet. It looks for the most recent transaction and extracts the memo.

Attackers like this approach for a few reasons:
1. Defenders cannot "sinkhole" the Solana blockchain.
2. If a C2 server at a specific IP is taken down, the attacker simply sends a new transaction to the Solana wallet with a new IP in the memo. The malware on thousands of infected machines will automatically pivot to the new server on its next check-in.
3. The malware’s traffic to Solana RPC nodes looks like legitimate cryptocurrency activity, which is common on developer machines, making it harder to flag as "malicious" by simple traffic analysis.

## Attack Simulation
Let's do a benign test. We will use the Solana devnet instead of api.mainnet as with devnet they will give you test SOL money to play with. Additionally, you don't need to setup an account, just use the Solana CLI to create everything. We will make a python script that will simulate a malware implant that will poll the test wallet we create every ten seconds for any new transactions, then run whatever is in the memo field of our transaction. 

I am using windows 11. Let's start by installing the Solana CLI

Run CMD as Admin
```
curl https://release.anza.xyz/stable/solana-install-init-x86_64-pc-windows-msvc.exe --output C:\solana-install-tmp\solana-install-init.exe --create-dirs
```
To install run: 
```
C:\solana-install-tmp\solana-install-init.exe v1.18.22
```
Close the terminal and reopen as admin. Verify with: 
```
solana --version
```
Generate a new wallet
```
solana-keygen new --outfile $HOME\my-test-wallet.json
```
Set it as the default wallet
```
solana config set --keypair $HOME\my-test-wallet.json
```
Get your public address 
```
solana address
```
Configure solana to use devnet as it will give you free SOL for testing
```
solana config set --url https://api.devnet.solana.com
```
To airdrop some free SOL, go here: https://faucet.solana.com/  I found that it only works if you link your GitHub, so I did that, put my wallet address in and chose 2.5 for amount.

Check your balance
```
solana balance
```

To test, ill do a print of the words, "this is a test" and also creating a file. For the command below I use a made up wallet, change that to your wallet. 

```
solana transfer B8nfzR3suV5N2mLBUBtwtmxS1AHFGYjthqog1nFdefGE 0.001 --allow-unfunded-recipient --fee-payer $HOME\my-test-wallet.json --with-memo "PRINT_TEST" --url https://api.devnet.solana.com
```

This should give you a signature, like Signature: Zri6PMXRgFwD3BQ9VhUu7pBa2Ly1x2nmzuZHSmeB1i8cM7MFN6VWctseq8KdpVzYUctqyMYm66vtMTZYGnUayHV3

Install python https://www.python.org/downloads/release/pymanager-260/  Then install requirements:
```
python -m pip install solana solders
```

Create this script:
```
import time
import os
from solana.rpc.api import Client
from solders.pubkey import Pubkey

# Configuration
SOLANA_CLIENT = Client("https://api.devnet.solana.com")
# Replace with the public key from your my-test-wallet.json
WALLET_ADDRESS = Pubkey.from_string("B8nfzR3suV5N2mLBUBtwtmxS1AHFGYjthqog1nFdefGE")
HOME_DIR = os.path.expanduser("~")
CHECK_INTERVAL = 10  # Seconds

def execute_command():
    print("Action Triggered: this is a test")
    file_path = os.path.join(HOME_DIR, "c2_test_signal.txt")
    with open(file_path, "w") as f:
        f.write("Malware C2 Test Successful")
    print(f"File created at: {file_path}")

def monitor_wallet():
    print(f"Monitoring {WALLET_ADDRESS} for C2 instructions...")
    last_signature = None

    while True:
        try:
            # Get the most recent signatures for the wallet
            response = SOLANA_CLIENT.get_signatures_for_address(WALLET_ADDRESS, limit=1)
            
            if response.value:
                current_signature = response.value[0].signature
                
                if current_signature != last_signature:
                    print(f"New transaction detected: {current_signature}")
                    
                    # Fetch transaction details to find the "instruction"
                    tx_details = SOLANA_CLIENT.get_transaction(current_signature, max_supported_transaction_version=0)
                    
                    # Search for the "PRINT_TEST" string in logs or memo instructions
                    log_messages = str(tx_details.value.transaction.meta.log_messages)
                    
                    if "PRINT_TEST" in log_messages:
                        execute_command()
                    
                    last_signature = current_signature
        
        except Exception as e:
            print(f"Error: {e}")
            
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_wallet()
```

Then run it:
```
c:\Users\ljenkins\Documents\solana-test>python3 solana-test.py
```
It should look like:
```
Monitoring B8nfzR3suV5N2mLBUBtwtmxS1AHFGYjthqog1nFdefGE for C2 instructions...
New transaction detected: 5tu6PMXRgFwD3BQ9VhUu7pBa2Ly1x2nmzuZHSmeB1i8cM7MFN6VWctseq8KdpVzYUctqyMYm66vtMTZYGnUayHV3
Action Triggered: this is a test
File created at: C:\Users\ljenkins\c2_test_signal.txt
```








