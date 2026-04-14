from flask import Flask, request
import json
import os

app = Flask(__name__)

# Конфигурация из переменных окружения
CONFIRMATION_TOKEN = os.environ.get('CONFIRMATION_TOKEN', '2dc82528')

@app.route('/', methods=['POST'])
def handle_webhook():
    data = request.json
    # 1. Мгновенно отвечаем на confirmation
    if data.get('type') == 'confirmation':
        return CONFIRMATION_TOKEN
    # 2. На все остальные запросы сразу возвращаем 'ok'
    #    Вся сложная логика будет выполняться после этого
    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
