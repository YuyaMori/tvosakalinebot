from flask import Flask, request, abort
import os

from linebot import (
    LineBotApi, WebhookHandler
)

from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

#環境変数取得
ACCESS_TOKEN ="ZBThz0WytHRHLBQl8nYXanKaSVIWCTMIA9T+wbvLQ+MMUek5m0OrCeaStfJ4Ue6NlPm9ELXd9BGcDMT1o7JSlyA5komJuFjbBc8NcWUjnSMUI1kTRsCa0ZH8lVnz0dd5QrbyDkApQtZrDiYdrwst2gdB04t89/1O/w1cDnyilFU="
SECRET = "4f453f19ba0886fcd1c65484715190e1"

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(SECRET)

@app.route("/")
def hello_world():
    return "hello world!"

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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)