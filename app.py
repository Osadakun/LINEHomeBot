import os
import sys
import json
from decimal import Decimal #金融系の計算で丸め誤差を排除するために必要なライブラリ

try:
    import cleardb
except:
    import pymysql
    pymysql.install_as_MySQLdb()
    import MySQLdb

from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import ( # 使用するモデル(イベント, メッセージ, アクションなど)を列挙
    FollowEvent, UnfollowEvent, MessageEvent, PostbackEvent,
    TextMessage, TextSendMessage, TemplateSendMessage,
    ButtonsTemplate, CarouselTemplate, CarouselColumn,
    PostbackTemplateAction
)

app = Flask(__name__)

ABS_PATH = os.path.dirname(os.path.abspath(sys.argv[0]))

CHANNEL_SECRET = os.environ['YOUR_CHANNEL_SECRET']
CHANNEL_ACCESS_TOKEN = os.environ['YOUR_CHANNEL_ACCESS_TOKEN']
REMOTE_HOST = os.environ['DB_HOSTNAME']
REMOTE_DB_NAME = os.environ['DB_NAME']
REMOTE_DB_USER = os.environ['DB_USERNAME']
REMOTE_DB_PASS = os.environ['DB_PASSWORD']
#REMOTE_DB_TB = os.environ['REMOTE_DB_TB']

if CHANNEL_SECRET is None:
    print('Specify LINE_CHANNEL_SECRET.')
    sys.exit(1)
if CHANNEL_ACCESS_TOKEN is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN.')
    sys.exit(1)

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

# https://アプリ名.herokuapp.com/test にアクセスしてtest okが表示されればデプロイ自体は成功してる
# flaskは@app.route("/ディレクトリ名")でルーティングする
@app.route("/test")
def test():
    return('test ok')

# LINE APIにアプリがあることを知らせるためのもの
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

# メッセージが来た時の反応
@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg)
    )
