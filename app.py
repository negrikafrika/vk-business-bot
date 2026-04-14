from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    data = request.json
    print("📩 Входящий запрос:", data)
    if data.get('type') == 'confirmation':
        print("🔑 Отправляем confirmation token")
        # Здесь должна быть ваша строка из VK
        return "2dc82528"
    return "ok"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
