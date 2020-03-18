#!/usr/bin/env python

import os
import json
import urllib.request
from chalice import Chalice
from chalice import Response
from linebot import LineBotApi
from linebot import WebhookHandler

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    StickerMessage, LocationMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    PostbackAction, PostbackEvent, StickerSendMessage,
    FlexSendMessage, QuickReply, QuickReplyButton)

from linebot.exceptions import InvalidSignatureError
from linebot.exceptions import LineBotApiError

app = Chalice(app_name='line-bot')

line_bot_api = LineBotApi(os.environ['LINEBOT_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['LINEBOT_CHANNEL_SECRET'])

# Flex Messeage(json)
payload = {
  "type": "flex",
  "altText": "Flex Message",
  "contents": 
#この下を書き換えます
  {
    "type": "bubble",
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": "hello, world"
        }
      ]
    }
  }
#この上を書き換えます
}


flex_obj = FlexSendMessage.new_from_json_dict(payload)

@app.route('/webhook', methods=['POST'])
def callback():
    signature = app.current_request.headers['X-Line-Signature']
    body = app.current_request.raw_body.decode('utf-8')
    try:
        handler.handle(body, signature)
    except InvalidSignatureError as e:
        return Response({'error': e.message}, status_code=400)
    return Response({'ok': True})

# MessageEvent (Text Message)
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    # 動作確認②
    if event.message.text == "クイックリプライ":
        # Quick Reply
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text='好きな食べ物は何ですか？',
                quick_reply=QuickReply(
                    items=[
                    QuickReplyButton(
                        action=PostbackAction(label="明太子", display_text="明太子", data="result-1")
                    ),
                    QuickReplyButton(
                        action=PostbackAction(label="ラーメン", display_text="ラーメン", data="result-2")
                    ),
                    QuickReplyButton(
                        action=PostbackAction(label="もつ鍋", display_text="もつ鍋", data="result-3")
                    ),
                    ]
                )
            )
        )
    # 動作確認③
    elif event.message.text == "フレックスメッセージ":
        # Flex Message
        line_bot_api.reply_message(
            event.reply_token,
            messages=flex_obj
        )
    # 動作確認④
    elif event.message.text == "チェンジ":
        # アイコンおよび表示名を変更する
        change_icon_and_display_name(event, "ライオン","https://www.dl.dropboxusercontent.com/s/mgy1uh974u847lx/18576284415_fba4763805_q.jpg")
    # 動作確認①    
    else:
        # オウム返し
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )
    
# Postback Event
@handler.add(PostbackEvent)
def handle_post_back(event):
    if event.postback.data == "result-1":
        line_bot_api.reply_message(
            event.reply_token,
            StickerSendMessage(
                package_id="11537",
                sticker_id="52002734"
            )
        )
    elif event.postback.data == "result-2":
        line_bot_api.reply_message(
            event.reply_token,
            StickerSendMessage(
                package_id="11537",
                sticker_id="52002735"
            )
        )
    elif event.postback.data == "result-3":
        line_bot_api.reply_message(
            event.reply_token,
            StickerSendMessage(
                package_id="11537",
                sticker_id="52002736"
            )
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='すみません、該当するものがありません。')
        )

# MessageEvent (Other Message)
@handler.add(MessageEvent, message=(ImageMessage, VideoMessage, AudioMessage, StickerMessage, LocationMessage))
def handle_other_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='テキストを入力してください。')
    )

# Change icon and display name
def change_icon_and_display_name(event, name, icon_url):
    url = 'https://api.line.me/v2/bot/message/reply'
    data = {
        "replyToken": event.reply_token,
        "messages": [
            {
                "type": "text",
                "text": "こんにちは！私は" + name + "です!!",
                "sender": {
                    "name": name,
                    "iconUrl": icon_url
                }
            }
        ]
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+os.environ['LINEBOT_CHANNEL_ACCESS_TOKEN']
    }
    
    req = urllib.request.Request(url, json.dumps(data).encode(), headers)
    with urllib.request.urlopen(req) as res:
        body = res.read()
