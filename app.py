import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
import json
import os
from flask import Flask, request

# ========== НАСТРОЙКИ (через переменные окружения) ==========
TOKEN = os.environ.get('VK_TOKEN')            # Токен сообщества
CONFIRMATION_TOKEN = 'vk1.a.fp0aOwHumI9CXOTXhDsazPnOlvxboV3auWdLu_VZoyWR7ZqgjYpe3clTuafI09fk3_mzqN1s6mCYjmjO3RJohmMh5dArNxyZBJVs1VywKeEr1GwPBFkFZtszjYHqkaP-BR_IxvWqJ_85CSkUwP5MvqqMCKDBjEE4CKaSnXRdY4XswoGi4AJ-dOC2cZD0JJs0-VB3X9T73zQrDKycALEBEA'  # Из настроек Callback API VK
GROUP_ID = os.environ.get('GROUP_ID')         # ID группы (число)
MANAGER_ID = os.environ.get('MANAGER_ID')     # VK ID менеджера

# ========== ИНИЦИАЛИЗАЦИЯ VK ==========
vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()

# ========== ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ ОТПРАВКИ ==========
def send_message(user_id, text, keyboard=None):
    params = {
        "user_id": user_id,
        "message": text,
        "random_id": random.randint(1, 2**31)
    }
    if keyboard:
        params["keyboard"] = keyboard.get_keyboard()
    vk.messages.send(**params)

# ========== КЛАВИАТУРЫ ==========
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

# ========== ОБРАБОТЧИКИ КОМАНД (ПОЛНЫЕ ТЕКСТЫ) ==========
def handle_start(user_id):
    text = (
        "🚀 Добро пожаловать в агентство по продвижению малого бизнеса!\n\n"
        "Мы помогаем расти вашему делу в соцсетях и на маркетплейсах.\n"
        "Выберите нужный раздел на кнопках ниже 👇"
    )
    send_message(user_id, text, get_main_keyboard())

def handle_prices(user_id):
    text = (
        "📊 **Наши услуги и цены**\n\n"
        "🛒 Ведение маркетплейсов (Ozon, WB, Яндекс.Маркет) — **12 000 ₽/мес**\n"
        "📱 Ведение соцсетей (Instagram, VK, Telegram) — **15 000 ₽/мес**\n"
        "🎯 Настройка и ведение рекламы (Таргет, Яндекс.Директ) — **12 000 ₽/мес**\n"
        "💎 **Комплексная подписка** (всё сразу) — **35 000 ₽/мес**\n\n"
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
        "ℹ️ **О компании**\n\n"
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
        "📸 **Примеры работ**\n\n"
        "🔹 Магазин детской одежды «Bambini» — рост продаж на Ozon в 3 раза за 2 месяца.\n"
        "🔹 Студия загара «SunCity» — +250 подписчиков в VK, 30 заявок за неделю.\n"
        "🔹 Интернет-магазин подарков — настройка рекламы, окупаемость 140%.\n\n"
        "Больше кейсов высылаем по запросу. Напишите менеджеру!"
    )
    send_message(user_id, text, get_back_keyboard())

def handle_faq(user_id):
    text = (
        "❓ **Часто задаваемые вопросы**\n\n"
        "1️⃣ *Сколько времени занимает запуск?*\n"
        "   — До 3 дней на анализ и стратегию, затем запуск.\n\n"
        "2️⃣ *Есть ли договор и гарантии?*\n"
        "   — Да, работаем по договору. Гарантируем выполнение KPI.\n\n"
        "3️⃣ *Можно ли сначала попробовать одну услугу?*\n"
        "   — Да, любой тариф можно подключить отдельно.\n\n"
        "4️⃣ *Как получить отчёт о работе?*\n"
        "   — Еженедельный отчёт в Google Sheets или PDF.\n\n"
        "Остались вопросы? Нажмите «Связаться с менеджером»."
    )
    send_message(user_id, text, get_back_keyboard())

def handle_back(user_id):
    send_message(user_id, "Возвращаемся в главное меню.", get_main_keyboard())

# ========== FLASK-ПРИЛОЖЕНИЕ ДЛЯ ВЕБХУКОВ ==========
app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    data = request.json

    # Подтверждение сервера (обязательно)
    if data.get('type') == 'confirmation':
        return CONFIRMATION_TOKEN

    # Обработка нового сообщения
    if data.get('type') == 'message_new':
        msg_obj = data['object']['message']
        user_id = msg_obj['from_id']
        msg_text = msg_obj.get('text', '').lower().strip()
        payload = msg_obj.get('payload')

        cmd = None
        if payload:
            try:
                cmd = json.loads(payload).get('cmd')
            except:
                pass

        # Обработка команд из кнопок (payload)
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

        # Текстовые команды (если пользователь пишет вручную)
        elif msg_text in ['начать', '/start', 'старт', 'привет', 'меню']:
            handle_start(user_id)
        elif msg_text in ['услуги', 'цены', 'прайс', 'стоимость']:
            handle_prices(user_id)
        elif msg_text in ['менеджер', 'связаться', 'контакты']:
            handle_manager(user_id)
        elif msg_text in ['о нас', 'компания', 'информация']:
            handle_about(user_id)
        elif msg_text in ['примеры', 'портфолио', 'работы', 'кейсы']:
            handle_portfolio(user_id)
        elif msg_text in ['вопросы', 'faq', 'частые вопросы']:
            handle_faq(user_id)
        elif msg_text == 'назад':
            handle_back(user_id)
        else:
            send_message(
                user_id,
                "🤔 Я не понял. Напишите «начать», чтобы увидеть меню, или нажмите любую кнопку.",
                get_main_keyboard()
            )

    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)