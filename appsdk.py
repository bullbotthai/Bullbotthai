import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
#แก้เป็น * แต่จะมี error เยอะ
from linebot.models import *

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = '53049596e51a978c3a21fee5587aea52'
channel_access_token = 'SUoCA5pwOPSQ0LRMR2zuGeZTbg3nJtQJEGKVpTSTFJsgwuWfP6qPB06Pp179ar9lJayy6lvBaZBvqD+Ynx/sJqlzXo/4v0c6EMt7hsSWHCy1Q54vdjkfGb/ufXQi1bGPczfWuCLZPOe5jiette9uZwdB04t89/1O/w1cDnyilFU='
#เอามาจาก line developer
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

@app.route("/webhook", methods=['POST'])
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

@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    ### function reply token 
    
    Reply_token = event.reply_token
    text_fromUser = event.message.text

    # text_tosend_1 = TextSendMessage(text='BullBotThai',quick_reply=None)
    # text_tosend_2 = TextSendMessage(text='วันนี้เล่นตัวไหนดี',quick_reply=None)

    # line_bot_api.reply_message(
    #     Reply_token ,
    #     messages = [text_tosend_1, text_tosend_2]
    # )
    # image_message_1 = ImageMessage(
    #     origianl_content_url='xxx'
    #     ,preview_image_url='xxx' 
    # )
    if 'เช็คราคา' in text_fromUser:
        from Resource.bxAPI import GetBxPrice
        from random import randint

        num = randint(1,10)
        data = GetBxPrice(Number_to_get=num) ##เก็บจำนวนข้อมูล

        from Resource.FlexMessage import setbubble, setCarousel
        

        flex = setCarousel(data)

        from Resource.reply import SetMenuMessage_Object , send_flex

        flex = SetMenuMessage_Object(flex)
        send_flex(Reply_token, file_data = flex, bot_access_key = channel_access_token)


    else:
        text_list = [
            'ฉันไม่เข้าใจที่คุณพูด กรุณาเลือกใหม่อีกครั้ง',
            'ขออภัยฉันไม่เข้าใจจริงๆ ลองใหม่อีกครั้ง',
            'ขอโทษครับ ไม่ทราบว่าหมายความว่าอะไร',
            'กรุณากรอกข้อมูลใหม่อีกครั้งนึง'

        ]
        from random import choice
        text_data = choice(text_list)
        text_random = TextSendMessage(text=text_data)
        line_bot_api.reply_message(Reply_token,text_random)

@handler.add(FollowEvent)
def RegisRichmenu(event):
    userid = event.source.user_id
    disname = line_bot_api.get_profile(user_id=userid).display_name

    button_1 = QuickReplyButton(action=MessageAction(label='เช็คราคา',text='เช็คราคา'))
    button_2 = QuickReplyButton(action=MessageAction(label='เช็คข่าวสาร',text='เช็คข่าวสาร'))
    qbtn = QuickReply(items=[button_1,button_2])

    text = TextSendMessage(text='สวัสดีคุณ {} ยินดีต้อนรับสู่บริการแชตบอท'.format(disname))
    text_2 = TextSendMessage(text='กรุณาเลือกเมนูที่ท่านต้องการ',quick_reply= qbtn)

    line_bot_api.link_rich_menu_to_user(userid,'richmenu-91b306b4b5800d9c18ecbdf54c2df553')

    line_bot_api.reply_message(event.reply_token,messages=[text,text_2])

if __name__ == "__main__":
    app.run(port=200)
