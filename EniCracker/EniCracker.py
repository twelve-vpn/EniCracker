import logging
import os
import platform
import subprocess
import sys
import time
import requests
from dotenv import load_dotenv
from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes, Bip39WordsNum

class WalletGenerator:
    """Generates wallets and checks balances for multiple cryptocurrencies."""
    
    def __init__(self, config):
        self.config = config
        load_dotenv(self.config['ENV_FILE_PATH'])
        self.validate_env_vars()
        self.setup_logging()
        # Novas configurações para controle das redes
        self.check_btc = os.getenv('CHECK_BTC', 'true').lower() == 'true'
        self.check_eth = os.getenv('CHECK_ETH', 'true').lower() == 'true'
        self.check_bsc = os.getenv('CHECK_BSC', 'true').lower() == 'true'
        self.check_avax = os.getenv('CHECK_AVAX', 'true').lower() == 'true'
        self.check_matic = os.getenv('CHECK_MATIC', 'true').lower() == 'true'


    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(self.config['LOG_FILE_PATH']),
                logging.StreamHandler(sys.stdout),
            ],
        )

    def validate_env_vars(self):
        required_env_vars = ["ETHERSCAN_API_KEY", "BSCSCAN_API_KEY", "MATICSCAN_API_KEY"]
        missing_vars = [var for var in required_env_vars if not os.getenv(var)]
        if missing_vars:
            raise EnvironmentError(f"Missing environment variables: {', '.join(missing_vars)}")

    @staticmethod
    def generate_mnemonic():
        return Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_12)

    @staticmethod
    def seed_to_address(seed, coin_type):
        seed_bytes = Bip39SeedGenerator(seed).Generate()
        bip44_mst_ctx = Bip44.FromSeed(seed_bytes, coin_type)
        bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
        return bip44_acc_ctx.PublicKey().ToAddress()

    def check_balance(self, address, api_url_template, api_key='', network_name=''):
        print(f"Verificando | Endereço: {address} | Rede: {network_name}")
        try:
            api_url = api_url_template.format(address=address, api_key=api_key)
            response = requests.get(api_url)
            data = response.json()

            # Log da resposta da rede
            print(f"Resposta da rede {network_name}: {data}")

            # Tratamento para respostas de APIs que não usam a chave 'status' (como o Blockchain.info para Bitcoin)
            if address in data:
                balance = data[address]['final_balance'] / 1e8  # Para Bitcoin, convertendo de Satoshi para BTC
                print(f"Valor recebido para {network_name}: {balance} BTC")
                return balance

            # Tratamento para respostas padrão com 'status'
            elif 'status' in data and data['status'] == '1':
                balance = int(data['result']) / 1e18  # Para Ethereum e compatíveis, convertendo de Wei para ETH
                print(f"Valor recebido para {network_name}: {balance} ETH ou tokens compatíveis")
                return balance

            # Tratamento para erros de limite de taxa
            elif 'statusCode' in data and data['statusCode'] == 429:
                logging.error(f"Limite de taxa excedido para {address} na rede {network_name}: {data.get('message')}")
                return 0

            else:
                logging.error(f"Erro ao obter saldo para {address} na rede {network_name}: {data.get('message', 'Nenhuma mensagem')}")
                return 0

        except Exception as e:
            logging.error(f"Exceção ao verificar saldo para {address} na rede {network_name}: {str(e)}")
            return 0



    def write_wallet_info(self, seed, wallets):
        with open(self.config['WALLETS_FILE_PATH'], "a") as f:
            log_message = f"\nSeed: {seed}\n"
            for wallet in wallets:
                log_message += f"{wallet['type']} Address: {wallet['address']}, Balance: {wallet['balance']}\n"
            f.write(log_message)
            logging.info(f"Written to file: {log_message}")

def main():
    directory = os.path.dirname(os.path.abspath(__file__))
    config = {
        'LOG_FILE_PATH': os.path.join(directory, "EniCracker.log"),
        'ENV_FILE_PATH': os.path.join(directory, "EniCracker.env"),
        'WALLETS_FILE_PATH': os.path.join(directory, "wallets_with_balance.txt"),
    }
    generator = WalletGenerator(config)

    try:
        while True:
            seed = generator.generate_mnemonic()
            wallets_info = []

            # BTC
            if generator.check_btc:
                btc_address = generator.seed_to_address(seed, Bip44Coins.BITCOIN)
                btc_balance = generator.check_balance(btc_address, "https://blockchain.info/balance?active={address}", network_name="BTC")
                if btc_balance > 0:
                    wallets_info.append({'type': 'BTC', 'address': btc_address, 'balance': btc_balance})

            # ETH
            if generator.check_eth:
                eth_address = generator.seed_to_address(seed, Bip44Coins.ETHEREUM)
                eth_balance = generator.check_balance(
                    eth_address,
                    "https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey=" + os.getenv("ETHERSCAN_API_KEY"),
                    network_name="ETH"
                )
                if eth_balance > 0:
                    wallets_info.append({'type': 'ETH', 'address': eth_address, 'balance': eth_balance})

            # BSC
            if generator.check_bsc:
                bsc_balance = generator.check_balance(
                    eth_address,
                    "https://api.bscscan.com/api?module=account&action=balance&address={address}&apikey=" + os.getenv("BSCSCAN_API_KEY"),
                    network_name="BSC"
                )
                if bsc_balance > 0:
                    wallets_info.append({'type': 'BSC', 'address': eth_address, 'balance': bsc_balance})

            # AVAX
            if generator.check_avax:
                avax_balance = generator.check_balance(
                    eth_address,
                    "https://api.snowtrace.io/api?module=account&action=balance&address={address}&tag=latest&apikey=", # Aqui, inclua a chave da API se necessário
                    network_name="AVAX"
                )
                if avax_balance > 0:
                    wallets_info.append({'type': 'AVAX', 'address': eth_address, 'balance': avax_balance})

            # MATIC
            if generator.check_matic:
                matic_balance = generator.check_balance(
                    eth_address,
                    "https://api.polygonscan.com/api?module=account&action=balance&address={address}&apikey=" + os.getenv("MATICSCAN_API_KEY"),
                    network_name="MATIC"
                )
                if matic_balance > 0:
                    wallets_info.append({'type': 'MATIC', 'address': eth_address, 'balance': matic_balance})


            # If any wallet has balance, write to file
            if wallets_info:
                generator.write_wallet_info(seed, wallets_info)

    except KeyboardInterrupt:
        logging.info("Program interrupted by user. Exiting...")

if __name__ == "__main__":
    main()
