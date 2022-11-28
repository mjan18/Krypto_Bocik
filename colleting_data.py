import pandas as pd
import time
from tradingview_ta import TA_Handler, Interval, Exchange
import sqlalchemy
from datetime import datetime, timedelta

#importing data from trading view
def createFrame():
    bitcoin = TA_Handler(
        symbol="BTCUSDTPERP",
        screener="crypto",
        exchange="BINANCE",
        interval=Interval.INTERVAL_5_MINUTES
        #interval=Interval.INTERVAL_1_MINUTE
    )
    #getting important indicators
    candle = bitcoin.get_indicators(["open[1]", "high[1]", "low[1]", "close[1]", "RSI[1]"])
    df = pd.DataFrame(candle, index=[0])
    df.columns = ["open", "high", "low", "close", "RSI"]
    return df

#creating database
def createDatabase():
    while True:
        frame = createFrame()
        frame = frame.astype(float)
        frame.to_sql("btcusdt", engine, if_exists='append', index=False)
        print(frame)
        time.sleep(60*5)
        #time.sleep(60)

#creating engine
engine = sqlalchemy.create_engine('sqlite:///C:\\Users\\Michal\\Desktop\\Portfolio_Projects\\Trading_bot\\BTCUSDTsource.db')

#if table exist, drop it
engine.execute("DROP table IF EXISTS btcusdt")

#starting taking data in the first minutes of new bar
while True:
    temp_time = datetime.now()
    if int(temp_time.strftime('%S')) == 10:
        temp_minute = temp_time.strftime('%M')
        temp_minute = temp_minute[1:]
        if temp_minute == '0' or temp_minute == '5':
            print(temp_time)
            print(datetime.now())
            break

#creating database
createDatabase()

