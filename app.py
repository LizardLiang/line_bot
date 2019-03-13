from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

from lxml import etree

import requests



app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('U8y83kp/oua8dGGGGxGaJtPHkPbH0EX5xsIPLSs5mei/WF1jiLLPuFJ3V13LmT8zDsdoXCrmbRfoDrT2mG6wjPaXGkPk+/DxKU4PHSUU1rZ1AMiE043ObnI6ZMyHJEb9HXvoW2zr/y96YvUORU+lYAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('de13dee56ac904472fb56653553ba55b')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    #int_message = int(event.message.text) #to convert a string to a int
    if "123" in event.message.text:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str("健三小")))
    elif "!movie-" in event.message.text:
        cut = event.message.text.split('-')
        cut_1 = find_movie(cut[1])
        if "find nothing" in cut_1:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str('無此電影場次')))
        else:
            reply_text = movie_sep(cut_1)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
    elif "慈孤觀音" in event.message.text:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str("輕者當日，重者七日\n你要對慈孤觀音有信心")))
        

        
@handler.add(JoinEvent)    
def handle_join(event):
    newcoming_text = "恭迎慈姑觀音 渡世靈顯四方"

    line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text=newcoming_text)
        )
    print("JoinEvent =", JoinEvent)
    
def movie_sep(string1):
    timetable_urL = 'http://www.atmovies.com.tw/showtime/'
    timetable_urL += string1
    timetable_urL += '/a02/'
    timetable_url = requests.get(timetable_urL)
    timetable_text = etree.HTML(timetable_url.text)
    timetable = timetable_text.xpath('//a[@href=\"/showtime/t02e13/a02/\"]')
    reply_text = ""
    for cnt in range(len(timetable)):
        timetable_1 = timetable[cnt].getparent()
        timetable_2 = timetable_1.getparent()
        timetable_3 = timetable_2.xpath('li')
        result_1 = list()
        for cnt_1 in range(len(timetable_3)):
            result = timetable_3[cnt_1].xpath('text()')
            result_1 += result
            result_1 += "\n"
            print(result)
        reply_text = reply_text.join(result_1)
    return reply_text
    

def find_movie(name):
    r_1 = requests.get('http://www.atmovies.com.tw/showtime/t02e13/a02/')
    r_2 = etree.HTML(r_1.text)
    r_3 = r_2.xpath('//li[@class=\"filmTitle\"]')
    for cnt in range(len(r_3)):
        r_4 = r_3[cnt].xpath('a')
        t_1 = r_4[0].xpath('text()')
        print(t_1)
        if name in t_1:
            t_2 = r_4[0].attrib['href']
            t_3 = t_2.split('/')
            return t_3[2]
            break
        else:
            t_2 = "find nothing"
    return t_2

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
