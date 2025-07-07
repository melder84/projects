import time
from coinbase.wallet.client import Client

# Coinbase API keys
api_key = "organizations/38a8d3fa-3157-4068-9990-d8adc2f6e5b0/apiKeys/96549b0f-dd62-4713-828a-7ee1a75ecbdf"
api_secret = """-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIPw6OLQ3Dnd05aUCrJxdmF3CVCRs9oTENzh3Fv4g5ZWWoAoGCCqGSM49
AwEHoUQDQgAEgkfd6m/vfhYE5svXbR4aMBFnC+wAdCaI+e0jTR+uLzoKDT34rNcO
hRoGsoMB324VAUryV1Xr9NaOCtpGdRm8Bw==
-----END EC PRIVATE KEY-----"""

# Initialize the Coinbase client
client = Client(api_key, api_secret)

def get_account(currency):
    """Fetch the account details for a specific currency."""
    try:
        accounts = client.get_accounts()
        if 'data' in accounts:
            for account in accounts['data']:
                if account['currency'] == currency:
                    return account
        else:
            print(f"No accounts data found: {accounts}")
    except Exception as e:
        print(f"Error fetching {currency} account: {e}")
    return None

def get_current_price():
    """Fetch the current price of SHIB in USDC."""
    try:
        price = client.get_spot_price(currency_pair='SHIB-USDC')
        if price and 'amount' in price:
            return float(price['amount'])
        else:
            print(f"Price data missing or invalid: {price}")
    except Exception as e:
        print(f"Error fetching current price: {e}")
    return None

def sell_shib_for_usdc(shib_amount):
    """Sell SHIB for USDC."""
    try:
        account = get_account('SHIB')
        if not account:
            return None
        account_id = account['id']
        sell_order = client.sell(account_id, amount=shib_amount, currency='SHIB')
        if sell_order and 'total' in sell_order and 'amount' in sell_order:
            return float(sell_order['total']['amount']) / float(sell_order['amount']['amount'])
        else:
            print(f"Sell order data missing or invalid: {sell_order}")
    except Exception as e:
        print(f"Error selling SHIB: {e}")
    return None

def buy_shib_with_usdc(usdc_amount):
    """Buy SHIB with USDC."""
    try:
        account = get_account('USDC')
        if not account:
            return None
        account_id = account['id']
        buy_order = client.buy(account_id, amount=usdc_amount, currency='USDC')
        if buy_order and 'total' in buy_order and 'amount' in buy_order:
            return float(buy_order['amount']['amount'])
        else:
            print(f"Buy order data missing or invalid: {buy_order}")
    except Exception as e:
        print(f"Error buying SHIB: {e}")
    return None

def execute_trades():
    """Execute trading strategy."""
    try:
        usdc_account = get_account('USDC')
        shib_account = get_account('SHIB')

        print(f"USDC account response: {usdc_account}")
        print(f"SHIB account response: {shib_account}")

        if not usdc_account or not shib_account:
            print("Error: One or both accounts are missing.")
            return

        usdc_balance = float(usdc_account['available_balance']['value'])
        shib_balance = float(shib_account['available_balance']['value'])

        print(f"USDC Balance: {usdc_balance}, SHIB Balance: {shib_balance}")

        initial_sell_price = None

        while True:
            current_price = get_current_price()
            print(f"Current price: {current_price}")
            if current_price is None:
                print("Failed to get current price, retrying in 60 seconds.")
                time.sleep(60)
                continue

            if shib_balance > 0 and initial_sell_price is None:
                target_sell_price = current_price + 0.30

                if current_price >= target_sell_price:
                    initial_sell_price = sell_shib_for_usdc(shib_balance)
                    if initial_sell_price:
                        usdc_balance += initial_sell_price * shib_balance
                        shib_balance = 0
                        print(f"Sold SHIB at {initial_sell_price}. Waiting to buy back at a lower price.")

            if initial_sell_price is not None:
                buy_back_price = initial_sell_price * 0.995
                stop_loss_price = initial_sell_price * 0.90

                if current_price <= buy_back_price:
                    bought_price = buy_shib_with_usdc(usdc_balance)
                    if bought_price:
                        shib_balance = usdc_balance / bought_price
                        usdc_balance = 0
                        initial_sell_price = None
                        print(f"Bought back SHIB at {bought_price}.")
                
                if current_price <= stop_loss_price:
                    print(f"Stop loss triggered. Current price: {current_price} is below stop loss price: {stop_loss_price}.")
                    initial_sell_price = None

            time.sleep(60)
    except Exception as e:
        print(f"Error in trade execution: {e}")

# Run the trading execution
execute_trades()
