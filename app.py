from flask import Flask, request
import requests

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = "ใส่_CHANNEL_ACCESS_TOKEN_ตรงนี้"
OPENAI_API_KEY = "ใส่_OPENAI_API_KEY_ตรงนี้"

@app.route("/webhook", methods=['POST'])
def webhook():
    data = request.json
    
    for event in data.get('events', []):
        if event['type'] == 'message' and event['message']['type'] == 'text':
            user_text = event['message']['text']
            reply_token = event['replyToken']

            ai_reply = ask_openai(user_text)
            reply_to_line(reply_token, ai_reply)

    return 'OK'

def ask_openai(text):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": text}
        ]
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=body
    )

    result = response.json()
    return result['choices'][0]['message']['content']

def reply_to_line(reply_token, text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }

    body = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "text",
                "text": text
            }
        ]
    }

    requests.post(
        "https://api.line.me/v2/bot/message/reply",
        headers=headers,
        json=body
    )

if __name__ == "__main__":
    app.run()
