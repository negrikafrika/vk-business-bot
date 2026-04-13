import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
import json
from flask import Flask, request

# ========== ВСТАВЬТЕ СВОИ ДАННЫЕ ==========
VK_TOKEN = "vk1.a.fp0aOwHumI9CXOTXhDsazPnOlvxboV3auWdLu_VZoyWR7ZqgjYpe3clTuafI09fk3_mzqN1s6mCYjmjO3RJohmMh5dArNxyZBJVs1VywKeEr1GwPBFkFZtszjYHqkaP-BR_IxvWqJ_85CSkUwP5MvqqMCKDBjEE4CKaSnXRdY4XswoGi4AJ-dOC2cZD0JJs0-VB3X9T73zQrDKycALEBEA"                # ваш токен сообщества
CONFIRMATION_TOKEN = "2dc82528"       # из скриншота
GROUP_ID = "237615107"                # ID группы (строка)
MANAGER_ID = "627273348"              # ваш VK ID (число)

# ========== ИНИЦИАЛИЗАЦИЯ VK ==========
vk_session = vk_api.VkApi(token=VK_TOKEN)
vk = vk_session.get_api()

def send_message(user_id, text, keyboard=None):
    params = {
        "user_id": user_id,
        "message": text,
        "random_id": random.randint(1, 2**31)
    }
    if keyboard:
        params["keyboard"] = keyboard.get_keyboard()
    vk.messages.send(**params)

def get_main_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button("💰 Услуги и цены", color=VkKeyboardColor.POSITIVE, payload=json.dumps({"cmd": "prices"}))
    keyboard.add_button("📞 Связаться с менеджером", color=VkKeyboardColor.PRIMARY, payload=json.dumps({"cmd": "manager"}))
    keyboard.add_line()
    keyboard.add_button("ℹ️ О нас", color=VkKeyboardColor.SECONDARY, payload=json.dumps({"cmd": "about"}))
    keyboard.add_button("📸 Примеры работ", color=VkKeyboardColor.SECONDARY, payload=json.dumps({"cmd": "portfolio"}))
    keyboard.add_line()
    keyboard.add_button("❓ Частые вопросы", color=VkKeyboardColor.SECONDARY, payload=json.dumps({"cmd": "faq"}))
    return keyboard

def get_back_keyboard():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("◀ Назад", color=VkKeyboardColor.SECONDARY, payload=json.dumps({"cmd": "back"}))
    return keyboard

def handle_start(user_id):
    text = "🚀 Добро пожаловать в агентство по продвижению малого бизнеса!\n\nВыберите нужный раздел на кнопках ниже 👇"
    send_message(user_id, text, get_main_keyboard())

def handle_prices(user_id):
    text = "📊 Наши услуги и цены:\n\n🛒 Маркетплейсы — 12 000 ₽/мес\n📱 Соцсети — 15 000 ₽/мес\n🎯 Реклама — 12 000 ₽/мес\n💎 Комплекс — 35 000 ₽/мес"
    send_message(user_id, text, get_back_keyboard())

def handle_manager(user_id):
    text = f"👨‍💼 Наш менеджер: [id{MANAGER_ID}|нажать сюда]"
    send_message(user_id, text, get_back_keyboard())

def handle_about(user_id):
    text = "ℹ️ О компании: команда маркетологов с 5-летним опытом."
    send_message(user_id, text, get_back_keyboard())

def handle_portfolio(user_id):
    text = "📸 Примеры работ: кейсы в разных нишах."
    send_message(user_id, text, get_back_keyboard())

def handle_faq(user_id):
    text = "❓ FAQ: запуск до 3 дней, работа по договору."
    send_message(user_id, text, get_back_keyboard())

def handle_back(user_id):
    send_message(user_id, "Главное меню.", get_main_keyboard())

# ========== FLASK-СЕРВЕР ==========
app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    data = request.json
    print("📩 Запрос:", data)

    if data.get('type') == 'confirmation':
        return CONFIRMATION_TOKEN

    if data.get('type') == 'message_new':
        msg = data['object']['message']
        user_id = msg['from_id']
        text = msg.get('text', '').lower()
        payload = msg.get('payload')
        cmd = None
        if payload:
            try:
                cmd = json.loads(payload).get('cmd')
            except:
                pass

        if cmd == 'prices':
            handle_prices(user_id)
        elif cmd == 'manager':
            handle_manager(user_id)
        elif cmd == 'about':
            handle_about(user_id)
        elif cmd == 'portfolio':
            handle_portfolio(user_id)
        elif cmd == 'faq':
            handle_faq(user_id)
        elif cmd == 'back':
            handle_back(user_id)
        elif text in ['начать', 'старт', 'привет']:
            handle_start(user_id)
        else:
            send_message(user_id, "Напишите 'начать'", get_main_keyboard())

    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
