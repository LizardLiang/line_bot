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
import random
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC
import user_id_app, drinks_app, porn_app, movie_app, user_proccess

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('U8y83kp/oua8dGGGGxGaJtPHkPbH0EX5xsIPLSs5mei/WF1jiLLPuFJ3V13LmT8zDsdoXCrmbRfoDrT2mG6wjPaXGkPk+/DxKU4PHSUU1rZ1AMiE043ObnI6ZMyHJEb9HXvoW2zr/y96YvUORU+lYAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('de13dee56ac904472fb56653553ba55b')

game_key = 0
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
    user_id = event.source.user_id
    message = TextSendMessage(text=event.message.text)
    _index = user_proccess.check_status(user_id)
    #int_message = int(event.message.text) #to convert a string to a int
    if event.message.text == "健":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str("健三小")))
    if "!movie" in event.message.text:
        user_proccess.set_status(user_id, 1)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str('請輸入要搜尋的電影')))
    if _index == 1:
        cut_1 = movie_app.find_movie(event.message.text) #去尋找電影
        user_proccess.clear_status(user_id)
        if "find nothing" in cut_1:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str('無此電影場次')))
        else:
            reply_text = movie_app.movie_sep(cut_1) #找到電影後，去找時刻
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
    if "慈孤觀音" in event.message.text:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str("輕者當日，重者七日\n你要對慈孤觀音有信心")))
    if "!訂票" in event.message.text:
        try:
            date = event.message.text.split('-')
        except ValueError:
            print("just book")
        if len(date) > 1 :
            b_url = movie_app.buy_ticket(date)
        else:
            b_url = movie_app.buy_ticket(0)
        if b_url == "find nothing":
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str("尚無此日期場次")))
        else :
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=b_url))
    if "!擲骰子" == event.message.text:
        if user_id == "U58e43cf60b31e2ed4a101db4cab57fa6":
            num = '6'
            text_num = "擲到的點數是: "
            text_num += str(num)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text_num))
        else:
            num = random.randint(1,6)
            text_num = "擲到的點數是: "
            text_num += str(num)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text_num))
    if "!十八拉" == event.message.text or "!十八啦" == event.message.text:
        num = random.randint(1,6)
        num_1 = random.randint(1,6)
        num_2 = random.randint(1,6)
        num_3 = random.randint(1,6)
        text_num = "擲到的點數是: "
        text_num = text_num + str(num) + '、' + str(num_1) + '、' + str(num_2) + '、' + str(num_3)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text_num))
    if "!終極密碼" == event.message.text:
        global game_key
        game_key = random.randint(1,1000)
        print(game_key)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str("終極密碼已佈署完成")))
    if "!猜" in event.message.text:
        game_num = event.message.text.split("-")
        if int(game_num[1]) > game_key:
            print(game_key)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str("太大了，幹")))
        elif int(game_num[1]) < game_key:
            print(game_key)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str("太小了，跟你雞雞一樣")))
        elif int(game_num[1]) == game_key:
            print(game_key)
            game_key = random.randint(1,1000)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str("爆了齁，再玩啊")))
    if "柏翰" in event.message.text:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str("汪汪汪")))
    if "!註冊" == event.message.text:
        user_index = user_id_app.check_user(user_id)
        if user_index == -1:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str("註冊成功")))
        else:
            reply_text = "你是第" + str(user_index) + "位註冊的使用者"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
    if "!+飲料" in event.message.text:
        drink_name = event.message.text.split("-")
        drink_num = drinks_app.add_drinks(drink_name[1], user_id)
        print("drink_num", drink_num)
        if drink_num == -1:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str("新增成功")))
        elif drink_num == 0:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str("已存在的飲料")))
    if "!抽飲料" == event.message.text:
        drink_name = drinks_app.random_drinks()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=drink_name))
    if "!上映中" == event.message.text:
        reply_text = movie_app.get_url()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = reply_text))
    if "!預告" in event.message.text:
        movie_name = event.message.text.split('-')
        if len(movie_name) < 2 or movie_name[1] == '':
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = '林志儒吃屎'))
        teaser_url = movie_app.get_teaser(movie_name[1])
        if teaser_url == "failed":
            reply_text = 'Your movie: ' + movie_name[1] + ' cannot be found' 
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = reply_text))
        else:
            reply_text = 'https://www.youtube.com/watch?v=' + teaser_url
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = reply_text))
    if '!+番號' in event.message.text:
        porn_url = event.message.text.split('-')
        if len(porn_url) < 2 or porn_url[1] == '':
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = '林志儒吃屎'))
        porn_status = porn_app.add_porn(porn_url[1])
        if porn_status == 'success':
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = '感謝老司機的帶路'))
        elif porn_status == 'exist':
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = '老司機翻車拉~~'))
    if '!抽番號' == event.message.text:
        porn_url = porn_app.row_porn()
        reply_text = '老司機帶你上路: ' + porn_url
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = reply_text))

        
@handler.add(JoinEvent)    
def handle_join(event): #加入群組，會回復
    newcoming_text = "恭迎慈孤觀音 渡世靈顯四方"

    line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text=newcoming_text)
        )
    print("JoinEvent =", JoinEvent)
    

def add_to_spread():
    GDriveJSON = 'FAMAX-ef61fdf82b20.json'
    GSpreadSheet = 'line-bot'
    while True:
        try:
            scope = ['https://spreadsheets.google.com/feeds']
            key = SAC.from_json_keyfile_name(GDriveJSON, scope)
            gc = gspread.authorize(key)
            worksheet = gc.open(GSpreadSheet).sheet1
        except Exception as ex:
            print('無法連線Google試算表', ex)
            sys.exit(1)
        textt=""
        textt+=event.message.text
        if textt!="":
            worksheet.append_row((datetime.datetime.now(), textt))
            print('新增一列資料到試算表' ,GSpreadSheet)
            return textt
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)