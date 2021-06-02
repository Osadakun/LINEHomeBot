import config
import psycopg2
from flask import Flask, render_template, g, request, abort
import os
import json

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, MessageAction, TemplateSendMessage,
    ButtonsTemplate,TextSendMessage)

app = Flask(__name__)

line_bot_api = LineBotApi(config.ACCESS_TOKEN)
handler = WebhookHandler(config.CHANNEL_SECRET)

stadict = {"$B5/$-$F$k(B":1,"$B?2$F$k(B":2,"$B2H$K$$$k(B":3,"$B;E;vCf(B":4,"$B2q5DCf(B":5,"$B;E;vCf(B($BLk$N(B)":6,"$BGc$$J*Cf(B":7,"$B1?E>Cf(B":8,"$BN}=,Cf(B":9,"$BM'C#$H$$$k(B":10,"$B29@t$$$k(B":11,"$B<x6HCf(B":12,"$B%i%\$$$k(B":13,"$B30?)Cf(B":14,"$B=P6PCf(B":15,"$B30=PCf(B":16}

confirm = {
    "type": "template",
    "altText": "this is a confirm template",
    "template": {
        "type": "confirm",
        "actions": [
            {
                "type": "message",
                "label": "$B$O$$(B",
                "text": "$B$O$$(B"
            },
            {
                "type": "message",
                "label": "$B$$$$$((B",
                "text": "$B$$$$$((B"
            }
        ],
        "text": "test"
    }
}

#confirm_obj = FlexSendMessage.new_from_json_dict(confirm)


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
    dsn = config.PG_URL
    conn = psycopg2.connect(dsn)
    cur = conn.cursor()
    cur.execute('SELECT * FROM Family_Member')
    return cur
    line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(UserID)
    )
#    cur.execue('COMMIT')


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
