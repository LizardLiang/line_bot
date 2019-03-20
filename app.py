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
import gspread, sys
from oauth2client.service_account import ServiceAccountCredentials as SAC
import user_id_app, drinks_app, porn_app, movie_app, user_proccess, theater_app, bus_app, train_app
from bs4 import BeautifulSoup

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
    #wks_th = theater_app.connect_to_sheet()
    wks_pro = user_proccess.connect_to_spread()
    user_id = event.source.user_id
    _index = user_proccess.check_status(user_id, wks_pro)
    if event.message.text == '!取消' or event.message.text == '!cancel':
        user_proccess.clear_status(user_id, wks_pro)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text= '取消指令'))
    elif _index == '1':
        wks_th = theater_app.connect_to_sheet()
        wks_pro = user_proccess.connect_to_spread()
        user_id = event.source.user_id
        user_proccess.clear_status(user_id, wks_pro)
        cut_1 = movie_app.find_movie(user_id, event.message.text, wks_th, wks_pro) #去尋找電影
        if 'find nothing' in cut_1:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str('找不到您的電影，或是影院')))
        else:
            reply_text = movie_app.movie_sep(user_id, cut_1, wks_pro) #找到電影後，去找時刻
            if reply_text == '-1':
                reply_text = '找不到您的電影，或是影院'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
    elif _index == '2':
        wks_th = theater_app.connect_to_sheet()
        wks_pro = user_proccess.connect_to_spread()
        user_id = event.source.user_id
        user_proccess.clear_status(user_id, wks_pro)
        reply_text = movie_app.set_location(user_id, event.message.text, wks_th, wks_pro)
        if reply_text == '-1':
            reply_text = '找不到您的電影，或是影院'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
    
    #int_message = int(event.message.text) #to convert a string to a int
    if event.message.text == "健":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str("健三小")))
        
    elif "!movie" == event.message.text:
        wks_pro = user_proccess.connect_to_spread()
        user_proccess.set_status(user_id, 1, wks_pro)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str('請輸入要搜尋的電影')))
        
    elif '!設地區' == event.message.text:
        wks_pro = user_proccess.connect_to_spread()
        user_proccess.set_status(user_id, 2, wks_pro)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str('請輸入要搜尋的地區')))
    elif '!電影院' == event.message.text:
        wks_th = theater_app.connect_to_sheet()
        reply_text = theater_app.list_theater(wks_th)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = reply_text))
        
    elif "慈孤觀音" in event.message.text:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str("輕者當日，重者七日\n你要對慈孤觀音有信心")))
        
    elif "!訂票" in event.message.text:
        try:
            date = event.message.text.split('-')
            if len(date) > 1 :
                b_url = movie_app.buy_ticket(date)
            else:
                b_url = movie_app.buy_ticket(0)
            if b_url == "find nothing":
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str("尚無此日期場次")))
            else :
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=b_url))
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text= '指令格式錯誤'))
        
            
    elif "!擲骰子" == event.message.text:
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
            
    elif "!十八拉" == event.message.text or "!十八啦" == event.message.text:
        num = random.randint(1,6)
        num_1 = random.randint(1,6)
        num_2 = random.randint(1,6)
        num_3 = random.randint(1,6)
        text_num = "擲到的點數是: "
        text_num = text_num + str(num) + '、' + str(num_1) + '、' + str(num_2) + '、' + str(num_3)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text_num))
        
    elif "!終極密碼" == event.message.text:
        global game_key
        game_key = random.randint(1,1000)
        print(game_key)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str("終極密碼已佈署完成")))
        
    elif "!猜" in event.message.text:
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
            
    elif "柏翰" in event.message.text:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str("汪汪汪")))
        
    elif "!註冊" == event.message.text:
        user_index = user_id_app.check_user(user_id)
        if user_index == -1:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str("註冊成功")))
        else:
            reply_text = "你是第" + str(user_index) + "位註冊的使用者"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
            
    elif "!+飲料" in event.message.text:
        drink_name = event.message.text.split("-")
        drink_num = drinks_app.add_drinks(drink_name[1], user_id)
        print("drink_num", drink_num)
        if drink_num == -1:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str("新增成功")))
        elif drink_num == 0:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str("已存在的飲料")))
            
    elif "!抽飲料" == event.message.text:
        drink_name = drinks_app.random_drinks()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=drink_name))
        
    elif "!上映中" == event.message.text:
        reply_text = movie_app.get_url()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = reply_text))
        
    elif "!預告" in event.message.text:
        movie_name = event.message.text.split('-')
        if len(movie_name) < 2 or movie_name[1] == '':
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = '林志儒吃屎'))
            return 0
        teaser_url = movie_app.get_teaser(movie_name[1])
        if teaser_url == "failed":
            reply_text = 'Your movie: ' + movie_name[1] + ' cannot be found' 
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = reply_text))
        else:
            reply_text = 'https://www.youtube.com/watch?v=' + teaser_url
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = reply_text))
    elif '!+番號' in event.message.text:
        porn_url = event.message.text.split('-')
        if len(porn_url) < 2 or porn_url[1] == '':
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = '林志儒吃屎'))
        porn_status = porn_app.add_porn(porn_url[1])
        if porn_status == 'success':
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = '感謝老司機的帶路'))
        elif porn_status == 'exist':
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = '老司機翻車拉~~'))
    elif '!抽番號' == event.message.text:
        porn_url = porn_app.row_porn()
        reply_text = '老司機帶你上路: ' + porn_url
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = reply_text))
    elif '!bus' in event.message.text:
        key = event.message.text.split(' ')
        url = bus_app.find_bus(key[1], key[2])
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text= url))
    elif "!火車" in event.message.text:
            cut = event.message.text.split('-')
            text_list = train_app.train(cut[1])
            message = ''
            for num_3 in range(len(text_list)):
                message = message + text_list[num_3]
                if num_3 % 7 == 6 :
                    message = message + '----------\n'
                    if len(message) > 1900 :
                        message = message + '\n可以加上+早上or下午or晚上解鎖更多時刻表'
                        message = message + "\n---------------------------------"
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=(message)))
                        break
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=(message)))   
    elif '!2020總統大選' in event.message.text:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=('票投國民黨\n韓導三民主義統一中國')))   

@handler.add(JoinEvent)    
def handle_join(event): #加入群組，會回復
    newcoming_text = "恭迎慈孤觀音 渡世靈顯四方"

    line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text=newcoming_text)
        )
    print("JoinEvent =", JoinEvent)
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)