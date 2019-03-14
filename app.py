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
from user_id_app import users

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
    #int_message = int(event.message.text) #to convert a string to a int
    if event.message.text == "健":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str("健三小")))
    if "!movie-" in event.message.text:
        cut = event.message.text.split('-') #拆出指令與電影名稱
        cut_1 = find_movie(cut[1]) #去尋找電影
        if "find nothing" in cut_1:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str('無此電影場次')))
        else:
            reply_text = movie_sep(cut_1) #找到電影後，去找時刻
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
    if "慈孤觀音" in event.message.text:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str("輕者當日，重者七日\n你要對慈孤觀音有信心")))
    if "!訂票" in event.message.text:
        try:
            date = event.message.text.split('-')
        except ValueError:
            print("just book")
        if len(date) > 1 :
            b_url = buy_ticket(date)
        else:
            b_url = buy_ticket(0)
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
    if "!潤娥" == event.message.text:
        imur_url = "https://imgur.com/8kbH05x"
        button_template_message =ButtonsTemplate(
                            thumbnail_image_url="https://www.mcdelivery.com.tw/tw/home.html",
                            title='Menu', 
                            text='Please select',
                            ratio="1.51:1",
                            image_size="cover",
                            actions=[
#                                PostbackTemplateAction 點擊選項後，
#                                 除了文字會顯示在聊天室中，
#                                 還回傳data中的資料，可
#                                 此類透過 Postback event 處理。
                                URITemplateAction(
                                    label='uri可回傳網址', uri='https://www.mcdelivery.com.tw/tw/home.html'
                                )
                            ]
                        )
        line_bot_api.reply_message(event.reply_token,TemplateSendMessage(alt_text="Template Example", template=button_template_message))
    if "!註冊" == event.message.text:
        user_index = users.check_user(user_id)
        
        

        
@handler.add(JoinEvent)    
def handle_join(event): #加入群組，會回復
    newcoming_text = "恭迎慈孤觀音 渡世靈顯四方"

    line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text=newcoming_text)
        )
    print("JoinEvent =", JoinEvent)
    
def movie_sep(string1):
    timetable_urL = 'http://www.atmovies.com.tw/showtime/'
    timetable_urL += string1 # -> 抓到的電影網址關鍵詞
    timetable_urL += '/a02/'
    timetable_url = requests.get(timetable_urL) #抓網站
    timetable_text = etree.HTML(timetable_url.text) #把抓到的網站，用HTML的方式轉成文檔
    timetable = timetable_text.xpath('//a[@href=\"/showtime/t02e13/a02/\"]') #透過這個去反推我要的電影時刻在哪裡
    reply_text = ""
    result_1 = list()
    for cnt in range(len(timetable)):
        timetable_1 = timetable[cnt].getparent() 
        timetable_2 = timetable_1.getparent() #電影時刻的父標籤
        timetable_3 = timetable_2.xpath('li') #找到時刻的標籤
        for cnt_1 in range(len(timetable_3)):
            result = timetable_3[cnt_1].xpath('text()') #轉為 string -> 但是不知道為啥是 list
            print(result)
            if len(result) != 0 and ' \r\n\t\t\t\t\t\t\t\t' not in result: #去掉空白的跟巨幕廳下面的換行符
                result_1 += result #把 list 合起來
                result_1 += "\n"
    reply_text = reply_text.join(result_1) #把 list 加到 string 裡面
    return reply_text
    

def find_movie(name):
    r_1 = requests.get('http://www.atmovies.com.tw/showtime/t02e13/a02/') #讀取樹林秀泰的網頁
    r_2 = etree.HTML(r_1.text)
    r_3 = r_2.xpath('//li[@class=\"filmTitle\"]') #讀出所有電影名稱
    for cnt in range(len(r_3)):
        r_4 = r_3[cnt].xpath('a')
        t_1 = r_4[0].xpath('text()') 
        if name in t_1: #比較電影名稱
            t_2 = r_4[0].attrib['href']
            t_3 = t_2.split('/')
            return t_3[2] #有找到的話，回傳網址
        else:
            t_2 = "find nothing" #沒找到的話，回傳nothing
    return t_2

def buy_ticket(date):
    r_1 = 'https://www.showtimes.com.tw/events?corpId=54'
    if date != 0 :
        r_1 += '&date=' + str(date[1]) + '/' + str(date[2]) + '/' + str(date[3])
    return r_1

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