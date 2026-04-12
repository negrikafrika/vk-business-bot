import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
import time
import json
import threading
from flask import Flask

# ========== НАСТРОЙКИ (ЗАМЕНИТЕ НА СВОИ) ==========
TOKEN = "vk1.a.fp0aOwHumI9CXOTXhDsazPnOlvxboV3auWdLu_VZoyWR7ZqgjYpe3clTuafI09fk3_mzqN1s6mCYjmjO3RJohmMh5dArNxyZBJVs1VywKeEr1GwPBFkFZtszjYHqkaP-BR_IxvWqJ_85CSkUwP5MvqqMCKDBjEE4CKaSnXRdY4XswoGi4AJ-dOC2cZD0JJs0-VB3X9T73zQrDKycALEBEA"               # Токен сообщества
GROUP_ID = 237615107                  # ID группы (число)
MANAGER_ID = 627273348             # VK ID менеджера

# ========== KEEP-ALIVE СЕРВЕР (Flask) ==========
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Бот VK работает!'

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# Запускаем Flask-сервер в отдельном потоке
flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

# ========== ИНИЦИАЛИЗАЦИЯ VK ==========
vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, GROUP_ID)

def send_message(user_id, text, keyboard=None):
    """Отправка сообщения с клавиатурой (если передана)"""
    params = {
        "user_id": user_id,
        "message": text,
        "random_id": random.randint(1, 2**31)
    }
    if keyboard:
        params["keyboard"] = keyboard.get_keyboard()
    vk.messages.send(**params)

# ========== КЛАВИАТУРЫ С PAYLOAD ==========
def get_main_keyboard():
    """Главное меню — каждая кнопка передаёт свою команду в payload"""
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
    """Клавиатура с кнопкой 'Назад' (возврат в главное меню)"""
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("◀ Назад", color=VkKeyboardColor.SECONDARY, payload=json.dumps({"cmd": "back"}))
    return keyboard

# ========== ОБРАБОТЧИКИ КОМАНД ==========
def handle_start(user_id):
    text = (
        "🚀 Добро пожаловать в агентство по продвижению малого бизнеса!\n\n"
        "Мы помогаем расти вашему делу в соцсетях и на маркетплейсах.\n"
        "Выберите нужный раздел на кнопках ниже 👇"
    )
    send_message(user_id, text, get_main_keyboard())

def handle_prices(user_id):
    text = (
        "📊 Наши услуги и цены:\n\n"
        "🛒 Ведение маркетплейсов (Ozon, WB, Яндекс.Маркет) — 12 000 ₽/мес\n"
        "📱 Ведение соцсетей (Instagram, VK, Telegram) — 15 000 ₽/мес\n"
        "🎯 Настройка и ведение рекламы (Таргет, Яндекс.Директ) — 12 000 ₽/мес\n"
        "💎 Комплексная подписка (всё сразу) — 35 000 ₽/мес\n\n"
        "✅ В стоимость входит: аналитика, контент, ежедневный отчёт, поддержка 24/7.\n"
        "Для точного расчёта под ваш бизнес нажмите «Связаться с менеджером»."
    )
    send_message(user_id, text, get_back_keyboard())

def handle_manager(user_id):
    text = (
        "👨‍💼 Наш менеджер ответит на все вопросы и подберёт индивидуальное решение.\n\n"
        f"✍️ Напишите ему прямо сейчас: [id{MANAGER_ID}|нажать сюда]"
    )
    send_message(user_id, text, get_back_keyboard())

def handle_about(user_id):
    text = (
        "ℹ️ О компании\n\n"
        "Мы — команда маркетологов, таргетологов и SMM-специалистов с 5-летним опытом.\n"
        "Помогаем малому бизнесу привлекать клиентов из соцсетей и маркетплейсов.\n\n"
        "📌 Наши принципы:\n"
        "• Прозрачная отчётность\n"
        "• Работа на результат\n"
        "• Индивидуальный подход\n\n"
        "💼 Более 50 успешных кейсов в нишах: одежда, услуги, товары для дома, e-commerce."
    )
    send_message(user_id, text, get_back_keyboard())

def handle_portfolio(user_id):
    text = (
        "📸 Примеры работ\n\n"
        "🔹 Магазин детской одежды «Bambini» — рост продаж на Ozon в 3 раза за 2 месяца.\n"
        "🔹 Студия загара «SunCity» — +250 подписчиков в VK, 30 заявок за неделю.\n"
        "🔹 Интернет-магазин подарков — настройка рекламы, окупаемость 140%.\n\n"
        "Больше кейсов высылаем по запросу. Напишите менеджеру!"
    )
    send_message(user_id, text, get_back_keyboard())

def handle_faq(user_id):
    text = (
        "❓ Часто задаваемые вопросы\n\n"
        "1️⃣ Сколько времени занимает запуск?\n"
        "   — До 3 дней на анализ и стратегию, затем запуск.\n\n"
        "2️⃣ Есть ли договор и гарантии?\n"
        "   — Да, работаем по договору. Гарантируем выполнение KPI.\n\n"
        "3️⃣ Можно ли сначала попробовать одну услугу?\n"
        "   — Да, любой тариф можно подключить отдельно.\n\n"
        "4️⃣ Как получить отчёт о работе?\n"
        "   — Еженедельный отчёт в Google Sheets или PDF.\n\n"
        "Остались вопросы? Нажмите «Связаться с менеджером»."
    )
    send_message(user_id, text, get_back_keyboard())

def handle_back(user_id):
    """Возврат в главное меню"""
    send_message(user_id, "Возвращаемся в главное меню.", get_main_keyboard())

# ========== ГЛАВНЫЙ ЦИКЛ ОБРАБОТКИ СООБЩЕНИЙ ==========
print("✅ Бот запущен и слушает сообщения...")

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        user_id = event.message.from_id
        msg_text = event.message.text.lower().strip()
        payload = event.message.payload

        # Пытаемся распарсить payload (если он есть)
        cmd = None
        if payload:
            try:
                data = json.loads(payload)
                cmd = data.get("cmd")
            except:
                pass

        # Обработка команд из payload (нажатия на кнопки)
        if cmd == "prices":
            handle_prices(user_id)
        elif cmd == "manager":
            handle_manager(user_id)
        elif cmd == "about":
            handle_about(user_id)
        elif cmd == "portfolio":
            handle_portfolio(user_id)
        elif cmd == "faq":
            handle_faq(user_id)
        elif cmd == "back":
            handle_back(user_id)

        # Если payload не было, обрабатываем текстовые команды (для ручного ввода)
        elif msg_text in ["начать", "/start", "старт", "привет", "меню"]:
            handle_start(user_id)
        elif msg_text in ["услуги", "цены", "прайс", "стоимость"]:
            handle_prices(user_id)
        elif msg_text in ["менеджер", "связаться", "контакты"]:
            handle_manager(user_id)
        elif msg_text in ["о нас", "компания", "информация"]:
            handle_about(user_id)
        elif msg_text in ["примеры", "портфолио", "работы", "кейсы"]:
            handle_portfolio(user_id)
        elif msg_text in ["вопросы", "faq", "частые вопросы"]:
            handle_faq(user_id)
        elif msg_text == "назад":
            handle_back(user_id)
        else:
            # Неизвестная команда
            send_message(
                user_id,
                "🤔 Я не понял. Напишите «начать», чтобы увидеть меню, или нажмите любую кнопку.",
                get_main_keyboard()
            )

        # Вывод в консоль для отладки
        print(f"[{time.strftime('%H:%M:%S')}] Пользователь {user_id}: {msg_text} (cmd={cmd})")