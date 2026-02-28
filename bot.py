import ccxt
import time

exchange = ccxt.coinbase()

previous_price = None

print("Signal bot gestart - geeft koop/verkoop advies")

while True:
    try:
        ticker = exchange.fetch_ticker('BTC-USD')
        price = ticker['last']
        
        if previous_price is not None:
            change = (price - previous_price) / previous_price * 100
            
            if change > 2:
                print(f"🔴 BTC ${price:,.0f} ↑ {change:.2f}% → **VERKOOP**")
            elif change < -2:
                print(f"🟢 BTC ${price:,.0f} ↓ {change:.2f}% → **KOOP**")
            else:
                print(f"BTC ${price:,.0f} ({change:+.2f}%) → HOLD")
        else:
            print(f"BTC prijs geladen: ${price:,.0f}")
            
        previous_price = price
        time.sleep(30)
    except Exception as e:
        print("Fout:", e)
        time.sleep(30)
