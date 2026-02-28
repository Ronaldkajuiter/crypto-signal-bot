import ccxt
import time

exchange = ccxt.coinbase()

print("Beste signal bot gestart - BTC + XRP (EMA + RSI)")

while True:
    try:
        for symbol in ['BTC-USD', 'XRP-USD']:
            ticker = exchange.fetch_ticker(symbol)
            price = ticker['last']
            print(f"{symbol} prijs: ${price:,.4f}")
        time.sleep(30)
    except Exception as e:
        print("Fout:", e)
        time.sleep(30)
