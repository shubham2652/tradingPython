from flask import Flask,redirect
import os
import threading
import requests
from bs4 import BeautifulSoup
app = Flask(__name__)
global bot_token
global bot_chatId
global fiveStarBuy
global fourStarBuy
global threeStarBuy
global twoStarBuy
global fiveStarSell
global fourStarSell
global threeStarSell
global twoStarSell
fiveStarBuy = {
    'scan_clause': '( {cash} ( [0] 5 minute close > [0] 5 minute open and [-1] 5 minute close > [-1] 5 minute open and [-2] 5 minute close > [-2] 5 minute open and [0] 5 minute close > [-1] 5 minute high and latest close > 100 and latest volume > 200000 and [-2] 5 minute close > latest vwap and [ -3 ] 5 minute close <= 1 day ago  vwap and latest close >= latest sma( latest close , 200 ) and latest close >= latest ema( latest close , 9 ) ) ) '
}
fourStarBuy = {
    'scan_clause': '( {cash} ( latest close >= latest ema( latest close , 200 ) and [0] 10 minute macd line( 26,12,9 ) > [0] 10 minute macd signal( 26,12,9 ) and [ -1 ] 10 minute macd line( 26,12,9 ) <= [ -1 ] 10 minute macd signal( 26,12,9 ) and [0] 30 minute ema( [0] 30 minute close , 200 ) >= latest ema( latest close , 200 ) and latest volume >= 200000 and latest close >= latest ema( latest close , 9 ) ) )'
}
threeStarBuy = {
    'scan_clause': '( {cash} ( latest close > 250 and latest volume > 250000 and latest "close - 1 candle ago close / 1 candle ago close * 100" >= 2 and latest supertrend( 7 , 3 ) < latest close and 1 day ago  supertrend( 7 , 3 ) <= 1 day ago  close and latest ema( latest close , 9 ) >= latest ema( latest close , 55 ) and latest ema( latest close , 9 ) < latest close ) ) '
}
twoStarBuy = {
    'scan_clause': '( {cash} ( [0] 5 minute close > [0] 5 minute open and [-1] 5 minute close > [-1] 5 minute open and [-2] 5 minute close > [-2] 5 minute open and [0] 5 minute close > [-1] 5 minute high and latest close > 100 and latest close >= latest sma( latest close , 200 ) and latest close >= latest ema( latest close , 9 ) and latest volume > 200000 ) ) '
}
fiveStarSell = {
    'scan_clause': '( {cash} ( [0] 5 minute close < [0] 5 minute open and [-1] 5 minute close < [-1] 5 minute open and [-2] 5 minute close < [-2] 5 minute open and [0] 5 minute high < [-1] 5 minute close and latest close > 100 and latest volume > 200000 and latest close < latest vwap and 1 day ago  close >= 1 day ago  vwap and latest close <= latest sma( latest close , 200 ) and latest close <= latest ema( latest close , 9 ) ) ) '
}
fourStarSell = {
    'scan_clause': '( {cash} ( [0] 5 minute close < [0] 5 minute open and [-1] 5 minute close < [-1] 5 minute open and [-2] 5 minute close < [-2] 5 minute open and [0] 5 minute high < [-1] 5 minute close and latest close > 100 and latest volume > 200000 and latest close <= latest vwap and latest close <= latest sma( latest close , 200 ) and latest close <= latest ema( latest close , 9 ) ) ) '
}
threeStarSell = {
    'scan_clause': '( {cash} ( [0] 5 minute close < [0] 5 minute open and [-1] 5 minute close < [-1] 5 minute open and [-2] 5 minute close < [-2] 5 minute open and [0] 5 minute high < [-1] 5 minute close and latest close > 100 and latest close <= latest sma( latest close , 200 ) and latest close <= latest ema( latest close , 9 ) and latest close <= latest vwap and latest "close - 1 candle ago close / 1 candle ago close * 100" >= 3 ) ) '
}
twoStarSell = {
    'scan_clause': '( {cash} ( [0] 5 minute close < [0] 5 minute open and [-1] 5 minute close < [-1] 5 minute open and [-2] 5 minute close < [-2] 5 minute open and [0] 5 minute high < [-1] 5 minute close and latest close > 100 and latest volume > 200000 and latest close <= latest sma( latest close , 200 ) and latest close <= latest ema( latest close , 9 ) ) ) '
}
bot_token='1667142589:AAGl2z7xxmTDI9E891ZiTiRu1U9hgF1NUg8'
bot_chatId='456331112'
def prepareAndSendMessage():
    link = "https://chartink.com/screener/3-continuous-green-candle"
    url = 'https://chartink.com/screener/process'
    with requests.Session() as s:
        r = s.get(link)
        soup = BeautifulSoup(r.text,"html.parser")
        csrf = soup.select_one("[name='csrf-token']")['content']
        s.headers['x-csrf-token'] = csrf
        r = s.post(url,data=fiveStarBuy)
        for item in r.json()['data']:
            bot_message = "Buy 5-STAR ***** \n" + item['name'] + "\n" + item['nsecode'] + "\n" + str(item['per_chg']) + "\n" + str(item['close']) + "\n" + str(item['volume'])
            send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatId + '&parse_mode=Markdown&text=' + bot_message
            requests.get(send_text)
    with requests.Session() as s:
        r = s.get(link)
        soup = BeautifulSoup(r.text,"html.parser")
        csrf = soup.select_one("[name='csrf-token']")['content']
        s.headers['x-csrf-token'] = csrf
        r = s.post(url,data=fourStarBuy)
        for item in r.json()['data']:
            bot_message = "Buy 4-STAR **** \n" + item['name'] + "\n" + item['nsecode'] + "\n" + str(item['per_chg']) + "\n" + str(item['close']) + "\n" + str(item['volume'])
            send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatId + '&parse_mode=Markdown&text=' + bot_message
            requests.get(send_text)
    with requests.Session() as s:
        r = s.get(link)
        soup = BeautifulSoup(r.text,"html.parser")
        csrf = soup.select_one("[name='csrf-token']")['content']
        s.headers['x-csrf-token'] = csrf
        r = s.post(url,data=threeStarBuy)
        for item in r.json()['data']:
            bot_message = "Buy 3-STAR *** \n" + item['name'] + "\n" + item['nsecode'] + "\n" + str(item['per_chg']) + "\n" + str(item['close']) + "\n" + str(item['volume'])
            send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatId + '&parse_mode=Markdown&text=' + bot_message
            requests.get(send_text)
    with requests.Session() as s:
        r = s.get(link)
        soup = BeautifulSoup(r.text,"html.parser")
        csrf = soup.select_one("[name='csrf-token']")['content']
        s.headers['x-csrf-token'] = csrf
        r = s.post(url,data=twoStarBuy)
        for item in r.json()['data']:
            bot_message = "Buy 2-STAR ** \n" + item['name'] + "\n" + item['nsecode'] + "\n" + str(item['per_chg']) + "\n" + str(item['close']) + "\n" + str(item['volume'])
            send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatId + '&parse_mode=Markdown&text=' + bot_message
            requests.get(send_text)
            
    with requests.Session() as s:
        r = s.get(link)
        soup = BeautifulSoup(r.text,"html.parser")
        csrf = soup.select_one("[name='csrf-token']")['content']
        s.headers['x-csrf-token'] = csrf
        r = s.post(url,data=fiveStarSell)
        for item in r.json()['data']:
            bot_message = "SELL 5STAR \n" + item['name'] + "\n" + item['nsecode'] + "\n" + str(item['per_chg']) + "\n" + str(item['close']) + "\n" + str(item['volume'])
            send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatId + '&parse_mode=Markdown&text=' + bot_message
            requests.get(send_text)
            
    with requests.Session() as s:
        r = s.get(link)
        soup = BeautifulSoup(r.text,"html.parser")
        csrf = soup.select_one("[name='csrf-token']")['content']
        s.headers['x-csrf-token'] = csrf
        r = s.post(url,data=fourStarSell)
        for item in r.json()['data']:
            bot_message = "SELL 4STAR \n" + item['name'] + "\n" + item['nsecode'] + "\n" + str(item['per_chg']) + "\n" + str(item['close']) + "\n" + str(item['volume'])
            send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatId + '&parse_mode=Markdown&text=' + bot_message
            requests.get(send_text)
        
    with requests.Session() as s:
        r = s.get(link)
        soup = BeautifulSoup(r.text,"html.parser")
        csrf = soup.select_one("[name='csrf-token']")['content']
        s.headers['x-csrf-token'] = csrf
        r = s.post(url,data=threeStarSell)
        for item in r.json()['data']:
            bot_message = "SELL 3STAR \n" + item['name'] + "\n" + item['nsecode'] + "\n" + str(item['per_chg']) + "\n" + str(item['close']) + "\n" + str(item['volume'])
            send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatId + '&parse_mode=Markdown&text=' + bot_message
            requests.get(send_text)

    with requests.Session() as s:
        r = s.get(link)
        soup = BeautifulSoup(r.text,"html.parser")
        csrf = soup.select_one("[name='csrf-token']")['content']
        s.headers['x-csrf-token'] = csrf
        r = s.post(url,data=twoStarSell)
        for item in r.json()['data']:
            bot_message = "SELL 2STAR \n" + item['name'] + "\n" + item['nsecode'] + "\n" + str(item['per_chg']) + "\n" + str(item['close']) + "\n" + str(item['volume'])
            send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatId + '&parse_mode=Markdown&text=' + bot_message
            requests.get(send_text)
    threading.Timer(900.0,prepareAndSendMessage).start()
            
threading.Timer(0.0,prepareAndSendMessage).start()
@app.route("/trade")
def index():
    prepareAndSendMessage()
    return "Successfull"

@app.route("/")
def croneJobs():
    prepareAndSendMessage()
    return "crone job started"

if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
    except:
        port = 8080
    app.run(host='192.168.43.184',port=port,debug=True)
