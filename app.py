from flask import Flask, request
import requests
import subprocess
import os 

app = Flask(__name__)

VERIFY_TOKEN = "tatiftlales2011"

PAGE_ACCESS_TOKEN = "EAAReV10vOr4BO7dZCrqM5lZCEbtf0D8M6akdB7uT7iwpibuleGOgOO4eHYiQy3ImdV8QNRD0iO2dnVBZB0s9DG3HvGq0yRVqx1q9iSGwR2JnFit4qrmZCgabVB8kEm1kOPmzIVu6SBktZBnxFqw3k4BqYDmVBpNoi7SC8E2K1XKZBkbBP41HVuZBNEgDUN10OTmWa4yujxsNGNwjsf7n7LB3ZCwe4QrVOJAKqZBMZD"

@app.route("/")
def home():
    return "✅ البوت يعمل! كل شيء تمام."

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # التحقق من التوكن
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge"), 200
        return "خطأ في التحقق", 403

    elif request.method == "POST":
        data = request.get_json()
        if data.get("object") == "page":
            for entry in data.get("entry", []):
                for messaging_event in entry.get("messaging", []):
                    sender_id = messaging_event["sender"]["id"]

                    if "message" in messaging_event:
                        message_text = messaging_event["message"].get("text", "")
                        if "facebook.com" in message_text:
                            # استخراج رابط الفيديو المباشر
                            try:
                                result = subprocess.run(
                                    ["yt-dlp", "-g", message_text],
                                    capture_output=True,
                                    text=True
                                )
                                video_url = result.stdout.strip().split("\n")[0]
                                if video_url.startswith("http"):
                                    send_message(sender_id, f"🎬 رابط التحميل المباشر:\n{video_url}")
                                else:
                                    send_message(sender_id, "❌ لم أتمكن من استخراج رابط الفيديو.")
                            except Exception as e:
                                send_message(sender_id, f"❌ خطأ أثناء التحميل:\n{str(e)}")
                        else:
                            send_message(sender_id, "📥 أرسل لي رابط فيديو من فيسبوك وسأعطيك رابط التحميل.")

        return "تم", 200

def send_message(recipient_id, message_text):
    url = "https://graph.facebook.com/v17.0/me/messages"
    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    response = requests.post(url, params=params, headers=headers, json=data)
    print("📤 تم إرسال الرسالة:", response.text)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
