#import config
import psycopg2
from flask import Flask, render_template, g, request, abort
import os

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

PG_URL = os.environ["DATABASE_URL"]
ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

#line_bot_api = LineBotApi(config.ACCESS_TOKEN)
#handler = WebhookHandler(config.CHANNEL_SECRET)

handler = WebhookHandler(CHANNEL_SECRET)
line_bot_api = LineBotApi(ACCESS_TOKEN)



@app.route("/")
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
    dsn = PG_URL
    conn = psycopg2.connect(dsn)
    cur = conn.cursor()
    cur.execute('SELECT * FROM Family_Member')
    for r in cur:
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=r)
        )
    cur.execue('COMMIT')


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
