# EniCracker

This repository is a fork of the original EnigmaCracker, with added support for new networks, including Bitcoin, Ethereum, Binance Smart Chain, Polygon, and Avalanche. The tool is designed for brute forcing cryptocurrency wallets, maintaining all original assets. The updated configuration now includes credentials for checking balances across these networks, alongside API keys for Etherscan, BscScan, and Polygonscan.

## **How it works?**

EniCracker advances the methodology of its predecessor, EnigmaCracker, by integrating brute force techniques with enhanced capabilities to decipher mnemonic phrases across a wider array of cryptocurrency networks. This fork introduces support for Bitcoin, Ethereum, Binance Smart Chain, Polygon, and Avalanche, broadening the scope of wallet security assessments.

Upon execution, EniCracker generates a mnemonic phrase— a 12-word sequence derived from a predefined list of 2048 possible words. This phrase, known as a seed phrase, is crucial for accessing and managing cryptocurrency wallets across different devices. The script employs the BIP39 protocol to generate these phrases, which are then used as the Master Seed for generating wallet addresses across various blockchains.

## Installation

Clone the repository using:

```bash
git clone https://github.com/DouveAlexandre/EniCracker
```
Remember to install the required libraries using:
```bash
pip install -r requirements.txt
```
## Configuration
Enhance your script's capabilities by adding the following environment variables in your EniCracker.env file:

```bash
CHECK_BTC=true
CHECK_ETH=true
CHECK_BSC=true
CHECK_AVAX=true
CHECK_MATIC=true
ETHERSCAN_API_KEY=api_here
BSCSCAN_API_KEY=api_here
MATICSCAN_API_KEY=api_here
```
Obtain API keys from Etherscan, BscScan, and Polygonscan to enable balance checks on the respective networks.
## Execution
Run EniCracker from the command line:

```bash
cd path/to/EniCracker
python EniCracker.py
```

## Updates
This fork introduces support for additional networks and implements new features to enhance the original EnigmaCracker tool's capabilities.

### Technical Workflow

1. **Mnemonic Generation**: Utilizing the `bip_utils` library, the script generates a BIP39 mnemonic. This 12-word phrase acts as the **Master Seed**, the cornerstone for generating cryptographic keys for cryptocurrency wallets.

2. **Wallet Address Generation**: The script converts the mnemonic into a seed and subsequently generates wallet addresses for supported cryptocurrencies—BTC, ETH, BSC, AVAX, and MATIC—following the BIP44 standard. This standard dictates a hierarchical structure for deterministic wallets, allowing for the generation of multiple addresses from a single seed.

3. **Balance Checking**: For each generated address, EniCracker queries blockchain explorers (via APIs like Etherscan for ETH, BscScan for BSC, and others for supported networks) to check for existing balances. This process helps identify potentially active wallets.

4. **Result Logging**: If a wallet with a balance is found, the script logs the mnemonic, wallet addresses, and their balances in a `wallets_with_balance.txt` file. This file serves as a record of all potentially valuable findings.

5. **Environment Variable Configuration**: Users can customize their search by enabling or disabling balance checks for specific cryptocurrencies via environment variables (`CHECK_BTC`, `CHECK_ETH`, etc.), alongside API keys for network-specific explorers. This flexibility allows users to tailor the brute force process to their specific interests or research needs.

6. **Continuous Operation**: Designed to run continuously, the script iterates through the generation and checking process, logging any wallets with balances it encounters. This approach maximizes the chances of discovering active wallets over time.

## ⚠️**Disclaimer**⚠️

This script is developed for educational and research purposes only.

**By using this code, you agree to the following:**

1. You will not use this code, in whole or in part, for malicious intent, including but not limited to unauthorized mining on third-party systems.
2. You will seek explicit permission from any and all system owners before running or deploying this code.
3. You understand the implications of running mining software on hardware, including the potential for increased wear and power consumption.
4. The creator of this script cannot and will not be held responsible for any damages, repercussions, or any negative outcomes that result from using this script.

If you do not agree to these terms, please do not use or distribute this code.


