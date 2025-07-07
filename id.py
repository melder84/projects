from coinbase.wallet.client import Client

# Coinbase API keys
api_key = "organizations/38a8d3fa-3157-4068-9990-d8adc2f6e5b0/apiKeys/e7ef57b9-87c3-4421-8c2c-bcdd56bac0a2"
api_secret = """-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIEmimA/ejwtFzOLLBQpio1Q5aKjh2UDHSIFdfidAmiOGoAoGCCqGSM49
AwEHoUQDQgAE60e8u7q2nNAssxNpHpYuAW3IKs+RkQWol/wuOZy+TRLBLxhH9J8f
IPtLEra5RH0vs1zQHH6Y7kA7o28aXhv4XA==
-----END EC PRIVATE KEY-----
"""

# Initialize the Coinbase client
client = Client(api_key, api_secret)

def get_payment_methods():
    try:
        payment_methods = client.get_payment_methods()
        for method in payment_methods['data']:
            print(f"ID: {method['id']}, Type: {method['type']}, Name: {method['name']}")
    except Exception as e:
        print(f"Error fetching payment methods: {e}")

def get_transactions():
    try:
        accounts = client.get_accounts()['data']
        for account in accounts:
            transactions = client.get_transactions(account['id'])['data']
            for transaction in transactions:
                print(f"ID: {transaction['id']}, Type: {transaction['type']}, Status: {transaction['status']}")
    except Exception as e:
        print(f"Error fetching transactions: {e}")

if __name__ == "__main__":
    get_payment_methods()
    get_transactions()
