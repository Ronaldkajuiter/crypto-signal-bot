import ccxt
import time
import pandas as pd
import pandas_ta as ta

exchange = ccxt.coinbase({
    'apiKey': os.getenv('COINBASE_API_KEY'),
    'secret': os.getenv('COINBASE_API_SECRET'),
    'enableRateLimit': True,
})

print("Auto-trader gestart - koopt/verkoopt automatisch (1% per trade)")

while True:
    try:
        for symbol in ['BTC-USD', 'XRP-USD']:
            bars = exchange.fetch_ohlcv(symbol, '5m', limit=100)
            df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['ema9'] = ta.ema(df['close'], length=9)
            df['ema21'] = ta.ema(df['close'], length=21)
            df['rsi'] = ta.rsi(df['close'], length=14)

            price = df['close'].iloc[-1]
            balance = exchange.fetch_balance()['total']['USD']

            if df['ema9'].iloc[-1] > df['ema21'].iloc[-1] and df['rsi'].iloc[-1] < 70:
                amount = (balance * 0.01) / price
                exchange.create_market_buy_order(symbol, amount)
                print(f"✅ KOOP {symbol} @ ${price}")

            elif df['ema9'].iloc[-1] < df['ema21'].iloc[-1] and df['rsi'].iloc[-1] > 30:
                amount = exchange.fetch_balance()[symbol.split('-')[0]] * 0.5
                exchange.create_market_sell_order(symbol, amount)
                print(f"❌ VERKOOP {symbol} @ ${price}")

        time.sleep(300)
    except Exception as e:
        print("Fout:", e)
        time.sleep(30)
