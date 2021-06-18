#-*- cording: utf-8 -*-
import config
import mylib
import conv
import psycopg2
from flask import Flask, render_template, g, request, abort
import os
import json
from linebot.models import *

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)

app = Flask(__name__)
line_bot_api = LineBotApi(config.ACCESS_TOKEN)
handler = WebhookHandler(config.CHANNEL_SECRET)

stadict = {"おはよう":1,"おやすみ":2,"在宅中":3,"仕事中":4,"仕事中【夜の】":5,"買い物中":6,"いってきます":7,"帰ります":8,"運転中":9,"友達といる":10,"練習中":11,"温泉いる":12,"授業中":13,"ラボいる":14,"外出中":15,"会議中":16}


@app.route("/")
def hello_world():
    return "HelloWorld!"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'
@handler.add(MessageEvent, message=TextMessage)
def response_message(event):
    UserID = event.source.user_id
    Text = event.message.text
    GID = 'Ca9dcb02f93abc60b5e7c428cfd94533a'
    user_name = mylib.SQL_name(config.PG_URL,'SELECT name FROM Family_Member where id = ',UserID)
    User_name = conv.conversion(user_name)
    if User_name == 'としき':
        f = ("./status_contents/brother.json")
        fo = open(f,"r",encoding="utf-8")
        fl = json.load(fo)
        line_bot_api.reply_message(event.reply_token,
                [
                    FlexSendMessage(alt_text='状態を選んでね',contents = fl)
                ]
        )
        fo.close()
        if len(Text) > 0:
            status = stadict[Text]
            Status = mylib.SQL_status(config.PG_URL,'SELECT name,status FROM Family_Member;', str(status),User_name)
            Status = conv.bsend(Status)
            messages = TextSendMessage(text = Status)
            line_bot_api.push_message(GID, messages = messages)

    elif User_name == 'おとう':
        f = ("./status_contents/father.json")
        fo = open(f,"r",encoding="utf-8")
        fl = json.load(fo)
        line_bot_api.reply_message(event.reply_token,
                [
                    FlexSendMessage(alt_text='状態を選んでね',contents = fl)
                ]
        )
        fo.close()
        if len(Text) > 0:
            status = stadict[Text]
            Status = mylib.SQL_status(config.PG_URL,'SELECT name,status FROM Family_Member;', str(status),User_name)
            Status = conv.bsend(Status)
            messages = TextSendMessage(text = Status)
            line_bot_api.push_message(GID, messages = messages)

    elif User_name == 'おかあ':
        f = ("./status_contents/mother.json")
        fo = open(f,"r",encoding="utf-8")
        fl = json.load(fo)
        line_bot_api.reply_message(event.reply_token,
                [
                    FlexSendMessage(alt_text='状態を選んでね',contents = fl)
                ]
        )
        fo.close()
        Text = event.message.text
        if len(Text) > 0:
            status = stadict[Text]
            Status = mylib.SQL_status(config.PG_URL,'SELECT name,status FROM Family_Member;', str(status),User_name)
            Status = conv.bsend(Status)
            messages = TextSendMessage(text = Status)
            line_bot_api.push_message(GID, messages = messages)
            
    elif User_name == 'なお':
        f = ("./status_contents/sister.json")
        fo = open(f,"r",encoding="utf-8")
        fl = json.load(fo)
        line_bot_api.reply_message(event.reply_token,
                [
                    FlexSendMessage(alt_text='状態を選んでね',contents = fl)
                ]
        )
        fo.close()
        if len(Text) > 0:   
            status = stadict[Text]
            Status = mylib.SQL_status(config.PG_URL,'SELECT name,status FROM Family_Member;', str(status),User_name)
            Status = conv.bsend(Status)
            messages = TextSendMessage(text = Status)
            line_bot_api.push_message(GID, messages = messages)
    
    else:
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text='あなたは誰')
            ]
        )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
