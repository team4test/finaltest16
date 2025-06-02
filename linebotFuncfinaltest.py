from flask import Flask
app = Flask(__name__)

from flask import request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, PostbackEvent,
    TextSendMessage, AudioSendMessage, VideoSendMessage,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, PostbackTemplateAction, URITemplateAction,
    CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn
)
from urllib.parse import parse_qsl

# 請替換為你的實際資料
line_bot_api = LineBotApi('uZlqUEKYTz9BtmNWxRflJVcj/HGbL0jGCff9mBAUHoa15EHlq7YXKmGS3vy/pyZyYh3/NW2Z94+xZojc0iYkwY5zDh55Du1lGcvZ/ABOnUOjG+1Sy6Od8aYkd0OkQtXp5L2SStcRLiFY9Py29f7fcwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('9c9f451a0b20d77bf823a9cbf27f964e')
baseurl = 'https://86e4-2001-b400-e353-3426-60df-c388-b541-d187.ngrok-free.app/static/'  # 靜態檔案網址

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(f"✅ 收到訊息：{event.message.text}")
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="我收到你的訊息囉"))
    mtext = event.message.text
    
    if mtext == '@傳送聲音':
        try:
            message = AudioSendMessage(
                original_content_url=baseurl + '8way.m4a',
                duration=20000
            )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發送聲音時發生錯誤！'))

    elif mtext == '@傳送影片':
        try:
            message = VideoSendMessage(
                original_content_url=baseurl + '8way.mp4',
                preview_image_url=baseurl + '8way.jpg'
            )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發送影片時發生錯誤！'))

    elif mtext == '@按鈕樣板':
        sendButton(event)
    elif mtext == '@確認樣板':
        sendConfirm(event)
    elif mtext == '@轉盤樣板':
        sendCarousel(event)
    elif mtext == '@圖片轉盤':
        sendImgCarousel(event)
    elif mtext == '@購買商品':
        sendPizza(event)
    elif mtext == '@yes':
        sendYes(event)

@handler.add(PostbackEvent)
def handle_postback(event):
    backdata = dict(parse_qsl(event.postback.data))
    if backdata.get('action') == 'buy':
        sendBack_buy(event, backdata)
    elif backdata.get('action') == 'sell':
        sendBack_sell(event, backdata)

def sendButton(event):
    try:
        message = TemplateSendMessage(
            alt_text='按鈕樣板',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.ibb.co/1Jz61Bys/IMG-1758.jpg',
                title='這是鍋貼',
                text='請選擇：',
                actions=[
                    MessageTemplateAction(label='文字訊息', text='@購買鍋貼'),
                    URITemplateAction(label='連結網頁', uri='https://www.8way.com.tw'),
                    PostbackTemplateAction(label='回傳訊息', data='action=buy')
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

def sendConfirm(event):
    try:
        message = TemplateSendMessage(
            alt_text='確認樣板',
            template=ConfirmTemplate(
                text='你確定要購買這項商品嗎？',
                actions=[
                    MessageTemplateAction(label='是', text='@yes'),
                    MessageTemplateAction(label='否', text='@no')
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

def sendCarousel(event):
    try:
        message = TemplateSendMessage(
            alt_text='轉盤樣板',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.ibb.co/1Jz61Bys/IMG-1758.jpg',
                        title='這是鍋貼',
                        text='第一個轉盤樣板',
                        actions=[
                            MessageTemplateAction(label='文字訊息一', text='賣鍋貼'),
                            URITemplateAction(label='連結八方雲集網頁', uri='https://www.8way.com.tw'),
                            PostbackTemplateAction(label='回傳訊息一', data='action=sell&item=鍋貼')
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.ibb.co/BWJ13x4/Unknown.jpg',
                        title='這是豆漿',
                        text='第二個轉盤樣板',
                        actions=[
                            MessageTemplateAction(label='文字訊息二', text='賣豆漿'),
                            URITemplateAction(label='連結八方雲集網頁' ,uri='https://i.ibb.co/BWJ13x4/Unknown.jpg'),
                            PostbackTemplateAction(label='回傳訊息二', data='action=sell&item=豆漿')
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

def sendImgCarousel(event):
    try:
        message = TemplateSendMessage(
            alt_text='圖片轉盤樣板',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://i.ibb.co/1Jz61Bys/IMG-1758.jpg',
                        action=MessageTemplateAction(label='文字訊息', text='賣鍋貼')
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.ibb.co/BWJ13x4/Unknown.jpg',
                        action=PostbackTemplateAction(label='回傳訊息', data='action=sell&item=豆漿')
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

def sendPizza(event):
    try:
        message = TextSendMessage(text='感謝您購買鍋貼，我們將盡快為您製作。')
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

def sendYes(event):
    try:
        message = TextSendMessage(text='感謝您的購買，\n我們將盡快寄出商品。')
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

def sendBack_buy(event, backdata):
    try:
        text1 = '感謝您購買我們的商品，我們將盡快為您製作。\n(action 的值為 ' + backdata.get('action') + ')'
        text1 += '\n(可將處理程式寫在此處。)'
        message = TextSendMessage(text=text1)
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

def sendBack_sell(event, backdata):
    try:
        message = TextSendMessage(text='點選的是賣 ' + backdata.get('item'))
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

if __name__ == '__main__':
    app.run()
