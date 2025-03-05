from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from llm.llm_connect import LLMConnector  # 引入 LLMConnectorimport ssl

# 初始化 Flask 應用
app = Flask(__name__)

# LINE Messaging API 配置 (直接使用 token 和 secret)
LINE_CHANNEL_ACCESS_TOKEN = "MUzguO7e5msnSTyVnkCPM2mQgwOxVVxYl8EPZ5NdzP6m96THAEYavLqQeR56vQrWMtYPI6ic+jPfeP+2/oZoCcPaeH/RHT9KzHN4b2fnkPiseYrKSpP/2Vd8fw8gRU7uwSDRnbhbinnY0HvJCR0aZAdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "ac2487b61b56c668a934140c7948adc0"

# 初始化 LINE 設置
configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 初始化 LLMConnector
llm_connector = LLMConnector(
    model="gpt-3.5-turbo",  # 或 "gpt-4"
    temperature=0.7
)

# 根路由，確認 Flask 應用正常運行
@app.route("/")
def home():
    return "Flask app is running!"

# 這是用來處理 LINE Webhook 請求的路由
@app.route("/callback", methods=['POST'])
def callback():
    """
    處理 LINE Webhook 請求
    """
    signature = request.headers.get('X-Line-Signature')
    
    if not signature:
        app.logger.error("Missing X-Line-Signature header")
        abort(400, description="Missing X-Line-Signature header")

    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    try:
        # 使用 WebhookHandler 驗證並解析事件
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.error("Invalid signature. Please check your channel access token/channel secret.")
        abort(400, description="Invalid signature")
    except Exception as e:
        app.logger.error(f"Unhandled error: {e}")
        abort(500, description="Unhandled error")

    return 'OK'

# 當接收到文字消息時，這個函數會被調用
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """
    處理來自用戶的文字消息
    """
    app.logger.info("Entering handle_message...")  # Debug：進入函數
    user_message = event.message.text.strip().lower()  # 獲取用戶消息並轉小寫
    app.logger.info(f"Received text: {user_message}")  # Debug：打印接收到的訊息

    # 預定義回應
    predefined_responses = {
        "hi": "Whatup",
        "missyou": "Awww! Miss you too!"
    }

    # 根據用戶輸入決定回應
    if user_message in predefined_responses:
        reply = predefined_responses[user_message]
    else:
        app.logger.info("Querying LLM...")
        reply = llm_connector.generate_response(user_message)  # 使用 LLM 生成回應

    # 回應用戶
    try:
        with ApiClient(configuration) as api_client:
            messaging_api = MessagingApi(api_client)
            response = messaging_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=reply)]
                )
            )
        app.logger.info(f"Replied: {reply}")  # Debug：確認回覆
        app.logger.info(f"Response: {response}")  # Debug：打印回應狀態
    except Exception as e:
        app.logger.error(f"Unhandled error in handle_message: {e}")

if __name__ == "__main__":
    # 啟動 Flask 應用
    app.run(debug=True, port=5002, host="0.0.0.0")
