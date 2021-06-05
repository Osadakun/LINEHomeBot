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

stadict = {"起きてる":1,"寝てる":2,"家にいる":3,"仕事中":4,"会議中":5,"仕事中(夜の)":6,"買い物中":7,"運転中":8,"練習中":9,"友達といる":10,"温泉いる":11,"授業中":12,"ラボいる":13,"外食中":14,"出勤中":15,"外出中":16}


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
    user_name = mylib.SQL_name(config.PG_URL,'SELECT name FROM Family_Member where id = ',UserID)
    user_name = conv.conversion(user_name)
    if user_name == 'としき':
        f = ("./brother.json")
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
            Status = mylib.SQL_status(config.PG_URL,'UPDATE Family_Member set status = AllStatus.status from AllStatus where AllStatus.id = ', str(status), UserID)
    else:
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text='なにそれ')
            ]
        )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
