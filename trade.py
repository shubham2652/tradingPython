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
fiveStarBuy = {
    'scan_clause': '( {cash} ( [0] 5 minute close > [0] 5 minute open and [-1] 5 minute close > [-1] 5 minute open and [-2] 5 minute close > [-2] 5 minute open and [0] 5 minute close > [-1] 5 minute high and latest close > 100 and latest volume > 200000 and [-2] 5 minute close > latest vwap and [ -3 ] 5 minute close <= 1 day ago  vwap and latest close >= latest sma( latest close , 200 ) and latest close >= latest ema( latest close , 9 ) ) ) '
}
fourStarBuy = {
    'scan_clause': '( {cash} ( [0] 5 minute close > [0] 5 minute open and [-1] 5 minute close > [-1] 5 minute open and [-2] 5 minute close > [-2] 5 minute open and [0] 5 minute close > [-1] 5 minute high and latest close > 100 and latest volume > 200000 and [-2] 5 minute close >= latest vwap and latest close >= latest sma( latest close , 200 ) and latest close >= latest ema( latest close , 9 ) ) )  '
}
threeStarBuy = {
    'scan_clause': '( {cash} ( [0] 5 minute close > [0] 5 minute open and [-1] 5 minute close > [-1] 5 minute open and [-2] 5 minute close > [-2] 5 minute open and [0] 5 minute close > [-1] 5 minute high and latest close > 100 and [-2] 5 minute close >= latest vwap and latest close >= latest sma( latest close , 200 ) and latest close >= latest ema( latest close , 9 ) and latest "close - 1 candle ago close / 1 candle ago close * 100" >= 3 ) ) '
}
twoStarBuy = {
    'scan_clause': '( {cash} ( [0] 5 minute close > [0] 5 minute open and [-1] 5 minute close > [-1] 5 minute open and [-2] 5 minute close > [-2] 5 minute open and [0] 5 minute close > [-1] 5 minute high and latest close > 100 and latest close >= latest sma( latest close , 200 ) and latest close >= latest ema( latest close , 9 ) and latest volume > 200000 ) ) '
}

bot_token='1667142589:AAGl2z7xxmTDI9E891ZiTiRu1U9hgF1NUg8'
bot_chatId='456331112'

def sessionProcess(link, url, payload, weight, call):
    with requests.Session() as s:
        r = s.get(link)
        soup = BeautifulSoup(r.text,"html.parser")
        csrf = soup.select_one("[name='csrf-token']")['content']
        s.headers['x-csrf-token'] = csrf
        r = s.post(url,data=payload)
        for item in r.json()['data']:
            bot_message = call + weight + "-STAR ***** \n" + item['name'] + "\n" + item['nsecode'] + "\n" + str(item['per_chg']) + "\n" + str(item['close']) + "\n" + str(item['volume'])
            print("BOT Message",bot_message)
            send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatId + '&parse_mode=Markdown&text=' + bot_message
            requests.get(send_text)
def prepareAndSendMessage():
    link = "https://chartink.com/screener/3-continuous-green-candle"
    url = 'https://chartink.com/screener/process'
    
    sessionProcess(link, url, fiveStarBuy, str(5), "BUY")
    sessionProcess(link, url, fourStarBuy, str(4), "BUY")
    sessionProcess(link, url, threeStarBuy, str(3), "BUY")
    sessionProcess(link, url, twoStarBuy, str(2), "BUY")
    
    threading.Timer(900.0,prepareAndSendMessage).start()
            
threading.Timer(0.0,prepareAndSendMessage).start()
@app.route("/trade")
def index():
    prepareAndSendMessage()
    return "Successfull"
@app.route("/")
def croneJobs():
    return "crone job started"
if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
    except:
        port = 8080
    app.run(host='192.168.43.184',port=port,debug=True)
