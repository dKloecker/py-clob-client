## py-clob-client

<a href='https://pypi.org/project/py-order-utils'>
    <img src='https://img.shields.io/pypi/v/py-order-utils.svg' alt='PyPI'/>
</a>

Python client for the Polymarket CLOB

### Installation

`pip install py-clob-client`

Intended for use with Python 3.9

### Usage

```py
host = "http://localhost:8080"
key = os.getenv("PK")
creds = ApiCreds(api_key=os.getenv("CLOB_API_KEY"), api_secret=os.getenv("CLOB_SECRET"), api_passphrase=os.getenv("CLOB_PASS_PHRASE"))
chain_id = 80001
client = ClobClient(host, key=key, chain_id=chain_id, creds=creds)

# Create and sign a limit order buying 100 YES tokens for 0.50c each
lim_order = client.create_limit_order(LimitOrderArgs(
    price=0.50,
    size=100.0,
    side=BUY,
    token_id="16678291189211314787145083999015737376658799626183230671758641503291735614088"
))

# Send it to the server
resp = client.post_order(lim_order)
print(resp)

# Initiate a market sell of 100 YES tokens
mkt_order = client.create_market_order(MarketOrderArgs(
    size=100.0,
    side=SELL,
    token_id="16678291189211314787145083999015737376658799626183230671758641503291735614088"
))

resp = client.post_order(mkt_order)
print(resp)
```

See [examples](examples/) for more