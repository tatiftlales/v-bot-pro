from flask import Flask, request
import requests
import subprocess

app = Flask(__name__)

VERIFY_TOKEN = "tatiftlales2011"
PAGE_ACCESS_TOKEN = "EAAReV10vOr4BO6ojoOjWkSbTZCPjY7HJf4AQJXyF4o6APlFCytMIXAHx91C7w2QDvwhdHmrhZAKX7E9hxIjAhWB1gHv0AZAuuOxxBXUG2oFgf303tfjHEbuZCKPmYFW9Jdifqt3QKoi6hL2nT5Q0FJzQZCJ7ZBRqduNT7E2T9PL6vhEoPB23fakz5MdoglZBK5G8XIZBTXNq7AZDZD"

@app.route("/", methods=['GET'])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "خطأ في التحقق"

@app.route("/", methods=['POST'])
def webhook():
    data = request.get_json()
    for entry in data['entry']:
        for messaging_event in entry['messaging']:
            sender_id = messaging_event['sender']['id']
            if messaging_event.get('message'):
                message_text = messaging_event['message'].get('text')
                if "facebook.com" in message_text:
                    # تحميل رابط الفيديو باستخدام yt-dlp
                    result = subprocess.run(['yt-dlp', '-g', message_text], capture_output=True, text=True)
                    video_url = result.stdout.strip()
                    send_message(sender_id, f"🔗 رابط التحميل المباشر للفيديو:\n{video_url}")
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
    app.run(port=5000, debug=True)
