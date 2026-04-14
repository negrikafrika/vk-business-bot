# Импортируем все необходимые библиотеки
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from flask import Flask, request, jsonify
import random
import json
import os

# --- 1. ЗАГРУЗКА НАСТРОЕК ИЗ ПЕРЕМЕННЫХ ОКРУЖЕНИЯ ---
# Здесь наш бот забирает ключи, которые мы спрятали в настройках Bothost.
VK_TOKEN = os.environ.get('VK_TOKEN')
VK_CONFIRMATION_TOKEN = os.environ.get('VK_CONFIRMATION')
VK_SECRET_KEY = os.environ.get('VK_SECRET')
GROUP_ID = os.environ.get('GROUP_ID')
MANAGER_ID = os.environ.get('MANAGER_ID')

# --- 2. ПРОВЕРКА НАСТРОЕК (САМОДИАГНОСТИКА) ---
# Это наш внутренний аудит. Если какой-то ключ не загрузился, бот сам скажет об этом в логах.
if not VK_TOKEN:
    print("❌ КРИТИЧЕСКАЯ ОШИБКА: VK_TOKEN не найден в переменных окружения!")
if not VK_CONFIRMATION_TOKEN:
    print("❌ КРИТИЧЕСКАЯ ОШИБКА: VK_CONFIRMATION_TOKEN не найден в переменных окружения!")
if not VK_SECRET_KEY:
    print("⚠️ ПРЕДУПРЕЖДЕНИЕ: VK_SECRET не задан. Проверка подписей не будет работать.")
if not GROUP_ID:
    print("⚠️ ПРЕДУПРЕЖДЕНИЕ: GROUP_ID не задан.")
if not MANAGER_ID:
    print("⚠️ ПРЕДУПРЕЖДЕНИЕ: MANAGER_ID не задан.")

# --- 3. ИНИЦИАЛИЗАЦИЯ VK API ---
# Настраиваем инструмент для отправки сообщений.
vk_session = vk_api.VkApi(token=VK_TOKEN)
vk = vk_session.get_api()

def send_message(user_id, text, keyboard=None):
    """Простая функция для отправки сообщения."""
    params = {"user_id": user_id, "message": text, "random_id": random.randint(1, 2**31)}
    if keyboard:
        params["keyboard"] = keyboard.get_keyboard()
    vk.messages.send(**params)

# --- 4. ВАШИ КЛАВИАТУРЫ ---
def get_main_keyboard():
    """Главное меню."""
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
    """Клавиатура для возврата назад."""
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("◀ Назад", color=VkKeyboardColor.SECONDARY, payload=json.dumps({"cmd": "back"}))
    return keyboard

# --- 5. ВАШИ ОБРАБОТЧИКИ КОМАНД ---
def handle_start(user_id):
    text = ("🚀 Добро пожаловать в агентство по продвижению малого бизнеса!\n\n"
            "Выберите нужный раздел на кнопках ниже 👇")
    send_message(user_id, text, get_main_keyboard())

def handle_prices(user_id):
    text = ("📊 Наши услуги и цены:\n\n"
            "🛒 Ведение маркетплейсов — 12 000 ₽/мес\n"
            "📱 Ведение соцсетей — 15 000 ₽/мес\n"
            "🎯 Настройка рекламы — 12 000 ₽/мес\n"
            "💎 Комплексная подписка — 35 000 ₽/мес")
    send_message(user_id, text, get_back_keyboard())

def handle_manager(user_id):
    text = f"👨‍💼 Напишите нашему менеджеру: [id{MANAGER_ID}|нажать сюда]"
    send_message(user_id, text, get_back_keyboard())

def handle_about(user_id):
    text = ("ℹ️ О компании: Команда профессионалов с 5-летним опытом.\n"
            "Прозрачная отчётность, работа на результат.")
    send_message(user_id, text, get_back_keyboard())

def handle_portfolio(user_id):
    text = "📸 Примеры работ: Мы успешно продвинули десятки проектов. Напишите менеджеру для кейсов!"
    send_message(user_id, text, get_back_keyboard())

def handle_faq(user_id):
    text = ("❓ Часто задаваемые вопросы:\n"
            "1️⃣ Запуск — до 3 дней.\n"
            "2️⃣ Работаем по договору.\n"
            "3️⃣ Любой тариф можно подключить отдельно.")
    send_message(user_id, text, get_back_keyboard())

def handle_back(user_id):
    send_message(user_id, "Возвращаемся в главное меню.", get_main_keyboard())

# --- 6. ГЛАВНЫЙ ВЕБ-СЕРВЕР (САМАЯ ВАЖНАЯ ЧАСТЬ) ---
app = Flask(__name__)

@app.route('/', methods=['POST'])
def handle_webhook():
    # 1. Сразу говорим в лог, что получили запрос от VK. Это ключевой момент для отладки!
    print("📩 Получен запрос от VK!")

    # 2. Получаем данные от VK в формате JSON.
    data = request.json
    print(f"📦 Содержимое запроса: {data}")

    # 3. Обрабатываем тип запроса 'confirmation' (подтверждение сервера)
    if data.get('type') == 'confirmation':
        # Здесь мы должны вернуть VK ту самую строку, которую он от нас ждёт.
        print("🔑 Отправляем confirmation token!")
        # Убедитесь, что переменная VK_CONFIRMATION_TOKEN загружена из окружения!
        return VK_CONFIRMATION_TOKEN

    # 4. Обрабатываем тип запроса 'message_new' (новое сообщение от пользователя)
    if data.get('type') == 'message_new':
        # Достаём из запроса всю информацию о сообщении и пользователе
        msg = data['object']['message']
        user_id = msg['from_id']
        msg_text = msg.get('text', '').lower().strip()
        payload = msg.get('payload')
        print(f"👤 Пользователь {user_id} прислал: '{msg_text}'")

        # Пытаемся получить команду из кнопки (payload)
        cmd = None
        if payload:
            try:
                cmd = json.loads(payload).get('cmd')
            except Exception as e:
                print(f"⚠️ Ошибка при разборе payload: {e}")

        # --- ЛОГИКА ОТВЕТА БОТА ---
        if cmd == 'prices': handle_prices(user_id)
        elif cmd == 'manager': handle_manager(user_id)
        elif cmd == 'about': handle_about(user_id)
        elif cmd == 'portfolio': handle_portfolio(user_id)
        elif cmd == 'faq': handle_faq(user_id)
        elif cmd == 'back': handle_back(user_id)

        elif msg_text in ['начать', 'старт', 'привет']: handle_start(user_id)
        elif msg_text in ['услуги', 'цены']: handle_prices(user_id)
        elif msg_text in ['менеджер', 'контакты']: handle_manager(user_id)
        elif msg_text == 'назад': handle_back(user_id)
        else:
            send_message(user_id, "🤔 Я не понял. Напишите «начать», чтобы увидеть меню.", get_main_keyboard())

    # 5. VK всегда ждёт ответ 'ok' после обработки запроса.
    return 'ok'

if __name__ == '__main__':
    # Запускаем сервер. Bothost сам позаботится о том, чтобы сделать его доступным извне.
    app.run(host='0.0.0.0', port=8080)
