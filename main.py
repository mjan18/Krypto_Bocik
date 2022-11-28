#finding trend
# wszystko chodzi o okreslenie granicy up i granicy down
#   jesli jest trend nieokreslony to pierwszy knot to jest granica i up i down

#   sprawdzam kolejna strzalke czy wybija granice
#       jesli nie wybija to trend zostaje
#       jesli wybija to zmieniam granice i przypisuje odpowiedni trend
#           sprawdzam czy nie jest tuz przy poprzedniej do 3
#                jesli tak to nie nie zmieniam drugiej granicy
#                  jesli nie to:
#                       ustawiam druga granice na min lub max ktore znajduje sie pomiedzy dwoma szczytami lub dolkami
#                       (np jesli wybil nowy wyierzcholek to szukam min miedzy dwoma wierzcholkami i ustawiam granice down)
#   powtarzam cykl

import pandas as pd
import mplfinance as mpf
import sqlalchemy
from datetime import datetime, timedelta

def candle_color(o, c):
    if o > c:
        return 'red'
    elif o < c:
        return 'green'
    else:
        return 'undefined'

    #moge przekazywac engine do zczytywania danych (jak juz bede mial rzeczywiste)
def firstTrendAndBoarder():
    # finding trend - it is all about borders
    trend = 'no'
    borderHigh = {}
    borderLow = {}
    
    # varuables for candle up and down
    numberUp = 0
    numberDown = 0
    
    #defining first trend and boarder, when the program just started
    
    length = len(df1)
    #tworze pomocnizca tablice pozniej jej nie bedzie bo bede operowal na danych z sql
    df = pd.DataFrame()
    for i in range(length): #tego fora zamieniam na "while True" i czytanie danych z sql
        df = pd.concat([df, df1.iloc[[i]]]) #to tez pomocnicze (sztuczna rzeczywistosc zbieranie danych )
        
        if trend == 'no':
            borderHigh = {'time': str(df.iloc[[-1]].index[0]), 'border': float(df.iloc[[-1]]['high'])}
            borderLow = {'time': str(df.iloc[[-1]].index[0]), 'border': float(df.iloc[[-1]]['low'])}
            trend = 'not_found'
            continue
        #finding if new candle dislocate my boarder
        tempHigh = float(df.iloc[[-1]]['high'])
        tempLow = float(df.iloc[[-1]]['low'])
        tempChange = 0
        if tempHigh > borderHigh['border']:
            borderHigh['border'] = tempHigh
            borderHigh['time'] = str(df.iloc[[-1]].index[0])
            trend = 'temp_up'
            tempChange += 1
        if tempLow < borderLow['border']:
            borderLow['border'] = tempLow
            borderHigh['time'] = str(df.iloc[[-1]].index[0])
            trend = 'temp_down'
            tempChange += 1
        # unidentified trend
        if tempChange == 2:
            trend = 'not_found'
        #if it is goung up / down, check if I get two red / green candle
        #if I have to the same candle colors, end function I found trend 
        color = candle_color(float(df.iloc[[-1]]['open']), float(df.iloc[[-1]]['close']))
        if trend == 'temp_up':
            if color == 'red':
                numberUp += 1
                if numberUp == 2:
                    trend = 'up'
                    return [trend, borderHigh, borderLow, i]#to i tylko dlatego ze dzialam na danych ktore juz mam
        if trend == 'temp_down':
            if color == 'green':
                numberDown += 1
                if numberDown == 2:
                    trend = 'down'
                return [trend, borderHigh, borderLow, i]#to i tylko dlatego ze dzialam na danych ktore juz mam


if __name__ == '__main__':
    
    engine = sqlalchemy.create_engine('sqlite:///C:\\Users\\Michal\\Desktop\\Portfolio_Projects\\Trading_bot\\BTCUSDTsource.db')
    df1 = pd.read_sql('btcusdt', engine)

    #cos sie stalo z data i jest duuupa :(
    # wiec sam dodaje jeden brakujacy wiersz
    line = pd.DataFrame({"open":16567.4, "high":16580.0, "low":16555.4, "close":16560, "RSI":45.65}, index=[32])
    df1 = pd.concat([df1.iloc[:31], line, df1.iloc[31:]]).reset_index(drop=True)
    #musze jeszcze dodac czas do zczytywania danych
    df1.index = pd.date_range('2022-11-24 17:30:00',periods=(len(df1)), freq='5min')

    #finding first trend
    #print(firstTrendAndBoarder())
    trend,  borderHigh, borderLow, temp_i = firstTrendAndBoarder()


    #function
    length = len(df1)
    #tworze pomocnizca tablice pozniej jej nie bedzie bo bede operowal na danych z sql
df = pd.DataFrame()
#tej tez nie bedzie bo musze miec wszystkie dane jakie zdazylem pobrac
for i in range(temp_i): #tego fora zamieniam na "while True" i czytanie danych z sql
        df = pd.concat([df, df1.iloc[[i]]]) #to tez pomocnicze (sztuczna rzeczywistosc zbieranie danych )
for i in range(temp_i + 1, length): #pomocnicze, jak bedzie to w funkcji to ona sie wykonuje raz i wychodzi
    df = pd.concat([df, df1.iloc[[i]]]) #wiec do funkcji musze przekazac parametry swieczki 
    
    #finding if new candle dislocate my boarder
    tempHigh = float(df.iloc[[-1]]['high'])
    tempLow = float(df.iloc[[-1]]['low'])
    tempChange = 0
    #borderTime = ''
    if tempHigh > borderHigh['border']:
        borderHigh['border'] = tempHigh
        trend = 'up'
        tempChange += 1
        
        # sprawdzam czy nie jest tuz przy poprzedniej do 3
        if not (borderHigh['time'] == str(df.iloc[[-2]].index[0]) or borderHigh['time'] == str(df.iloc[[-3]].index[0])):
            
        #zmieniam to zeby byl between border pomiedzy granicami ale nie wlacznie tylko nawiat otwrty (nie od 5:55 tylko od 6)
            borderFromTime = datetime.strptime(borderHigh['time'], '%Y-%m-%d %H:%M:%S')
            borderFromTime += timedelta(minutes=5)
            print(borderFromTime)
            dfBetweenBorder = df.loc[borderFromTime:]
            #zmienic to border zeby nie bralo od tej co mam tylko nastpnej swieczki
            betweenBorderMin = float(dfBetweenBorder['low'].min()) #nwn czy to musi byc jako float bo jest numpy float
            borderLow['border'] = betweenBorderMin
            print(f"borderLow['time'] = {borderLow['time']}")
            borderLow['time'] = str(dfBetweenBorder[dfBetweenBorder['low'] == betweenBorderMin].index[0])
            print(f"borderLow['time'] = {borderLow['time']}")
            #print(dfBetweenBorder)
            print(f"borderHigh['time'] = {borderHigh['time']}")
            print(str(df.iloc[[-1]].index[0]))
            
            print(f"zmiana tempHigh {trend}")
            

        borderHigh['time'] = str(df.iloc[[-1]].index[0])
        
    if tempLow < borderLow['border']:
        borderLow['border'] = tempLow
        trend = 'down'
        tempChange += 1
        
        if not (borderLow['time'] == str(df.iloc[[-2]].index[0]) or borderLow['time'] == str(df.iloc[[-3]].index[0])):
            borderFromTime = datetime.strptime(borderLow['time'], '%Y-%m-%d %H:%M:%S')
            borderFromTime += timedelta(minutes=5)
            print(borderFromTime)
            dfBetweenBorder = df.loc[borderFromTime:]
            #ustawiam druga granice na min lub max ktore znajduje sie pomiedzy dwoma szczytami lub dolkami
            #zmienic to border zeby nie bralo od tej co mam tylko nastpnej swieczki
            betweenBorderMax = float(dfBetweenBorder['high'].max()) #nwn czy to musi byc jako float bo jest numpy float
            borderHigh['border'] = betweenBorderMax
            print(f"borderHigh['time'] = {borderHigh['time']}")
            borderHigh['time'] = str(dfBetweenBorder[dfBetweenBorder['high'] == betweenBorderMax].index[0])
            print(f"borderHigh['time'] = {borderHigh['time']}")
            #print(dfBetweenBorder)
            print(f"borderLow['time'] = {borderLow['time']}")
            print(str(df.iloc[[-1]].index[0]))
            print(f"zmiana tempLow{trend}")
            
        borderLow['time'] = str(df.iloc[[-1]].index[0])
        
    # unidentified trend
    if tempChange == 2:
        trend = 'undefined'
    print(i)
