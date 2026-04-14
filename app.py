from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    print("🔔 ПОЛУЧЕН ЗАПРОС!")
    print(f"Метод: {request.method}")
    print(f"Данные: {request.data}")
    print(f"JSON: {request.json}")
    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
