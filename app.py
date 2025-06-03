from flask import Flask, request
import requests
import subprocess
import os

app = Flask(__name__)

VERIFY_TOKEN = "tatiftlales2011"
PAGE_ACCESS_TOKEN = "EAAReV10vOr4BO7dZCrqM5lZCEbtf0D8M6akdB7uT7iwpibuleGOgOO4eHYiQy3ImdV8QNRD0iO2dnVBZB0s9DG3HvGq0yRVqx1q9iSGwR2JnFit4qrmZCgabVB8kEm1kOPmzIVu6SBktZBnxFqw3k4BqYDmVBpNoi7SC8E2K1XKZBkbBP41HVuZBNEgDUN10OTmWa4yujxsNGNwjsf7n7LB3ZCwe4QrVOJAKqZBMZD"

@app.route("/webhook", methods=['GET'])
def verify():
    # التحقق من التوكن عند تفعيل الويب هوك من فيسبوك
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "خطأ في التحقق"

@app.route("/webhook", methods=['POST'])
def webhook():
    data = request.get_json()
    for entry in data.get('entry', []):
        for messaging_event in entry.get('messaging', []):
            sender_id = messaging_event['sender']['id']
            if messaging_event.get('message'):
                message_text = messaging_event['message'].get('text', '')
                if "facebook.com" in message_text:
                    # تحميل رابط الفيديو باستخدام yt-dlp
                    result = subprocess.run(['yt-dlp', '-g', message_text], capture_output=True, text=True)
                    video_url = result.stdout.strip()
                    if video_url:
                        send_message(sender_id, f"🔗 رابط التحميل المباشر للفيديو:\n{video_url}")
                    else:
                        send_message(sender_id, "عذراً، لم أتمكن من استخراج رابط الفيديو.")
    return "تم", 200

def send_message(recipient_id, message_text):
    url = "https://graph.facebook.com/v17.0/me/messages"
    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    requests.post(url, params=params, headers=headers, json=data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
