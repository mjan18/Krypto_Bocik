import pandas as pd
from tradingview_ta import TA_Handler, Interval, Exchange
import sqlalchemy
from datetime import datetime
import time

#deleting first row
def deleteRow(rows_num):
    while rows_num > 200: #think how much data do I need
        dele = sqlalchemy.text("DELETE FROM btcusdt WHERE open IN (SELECT open FROM btcusdt LIMIT 1)")
        engine.execute(dele)
        rows_num -= 1

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
def createDatabase(connection):
    #while True:
    frame = createFrame()
    frame = frame.astype(float)
    frame.to_sql("btcusdt", engine, if_exists='append', index=False)
    print(frame)
    #time.sleep(60*5) #think about better way to start program
    # checking if table exists and has enough rows to start deleting
#if sqlalchemy.inspect(engine).has_table('btcusdt'): #czy jest taka tabela
    my_query = sqlalchemy.select([sqlalchemy.func.count()]).select_from(sqlalchemy.text('btcusdt')) #COUNT rows
    rows_num = connection.execute(my_query).fetchall()[0][0]
    deleteRow(rows_num)#czy dac tutaj ifa na wejscie do funkcji?
    #time.sleep(60)


if __name__ == '__main__':
    #creating engine
    engine = sqlalchemy.create_engine('sqlite:///C:\\Users\\Michal\\Desktop\\Portfolio_Projects\\Trading_bot\\BTCUSDTsource.db')
    connection = engine.connect()
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
                #creating database
                createDatabase(connection)
                time.sleep(60)
    # sql = sqlalchemy.text("SELECT * from btcusdt")
    
    # # Fetch all the records
    # result = engine.execute(sql).fetchall()
    
    # # View the records
    # for record in result:
    #     print("\n", record)

 
