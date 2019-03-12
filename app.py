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
    if "健" in event.message.text:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str("健三小")))
    elif "!movie":
        movie_sep()

        
@handler.add(JoinEvent)    
def handle_join(event):
    newcoming_text = "謝謝邀請我這個機器來至此群組！！我會盡力為大家服務的～"

    line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text=newcoming_text)
        )
    print("JoinEvent =", JoinEvent)
    
def movie_sep():
    timetable_url = requests.get('http://www.atmovies.com.tw/showtime/fcen44154738/a02/')
    timetable_text = etree.HTML(timetable_url.text)
    timetable = timetable_text.xpath('//a[@href=\"/showtime/t02e13/a02/\"]')
    timetable_1 = timetable[0].getparent()
    timetable_2 = timetable_1.getparent()
    timetable_3 = timetable_2.xpath('li')
    for cnt_1 in range(3):
        result = etree.tostring(timetable_3[cnt_1])
        print(result)
    
    
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
