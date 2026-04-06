import logging
import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ========== НАСТРОЙКИ ==========
TOKEN = "Сюда токен вместо этого текста"
ADMIN_ID = 0123456789
# ===============================

# Эмодзи для оформления
EMOJIS = {
    'new': '🆕',
    'order': '📦',
    'user': '👤',
    'admin': '👨‍💼',
    'message': '✉️',
    'photo': '🖼️',
    'time': '⏰',
    'id': '🆔',
    'reply': '↩️',
    'success': '✅',
    'error': '❌',
    'warning': '⚠️',
    'info': 'ℹ️',
    'phone': '📱',
    'email': '📧',
    'location': '📍',
    'money': '💰',
    'delivery': '🚚',
    'check': '✅',
    'star': '⭐️',
    'heart': '❤️',
    'fire': '🔥',
    'rocket': '🚀',
    'gift': '🎁',
    'discount': '🏷️',
    'crown': '👑',
    'shield': '🛡️',
    'bell': '🔔',
    'lock': '🔒',
    'unlock': '🔓',
    'settings': '⚙️',
    'search': '🔍',
    'home': '🏠',
    'shop': '🏪',
    'cart': '🛒',
    'bag': '👜',
    'credit_card': '💳',
    'bank': '🏦',
    'receipt': '🧾',
    'calendar': '📅',
    'clock': '⏱️',
    'thumbs_up': '👍',
    'thumbs_down': '👎',
    'ok_hand': '👌',
    'clap': '👏',
    'wave': '👋',
    'point_right': '👉',
    'point_left': '👈',
    'point_up': '👆',
    'point_down': '👇',  # <-- ДОБАВИЛ ЭТО
    'up': '⬆️',
    'down': '⬇️',
    'left': '⬅️',
    'right': '➡️',
    'red_circle': '🔴',
    'green_circle': '🟢',
    'blue_circle': '🔵',
    'yellow_circle': '🟡',
    'purple_circle': '🟣',
}

# Хранилище для сообщений
user_messages = {}

# Красивое оформление текста
def format_welcome():
    return f"""{EMOJIS['rocket']} <b>ДОБРО ПОЖАЛОВАТЬ В НАШ МАГАЗИН!</b> {EMOJIS['rocket']}

{EMOJIS['star']} <b>Мы рады приветствовать вас!</b> {EMOJIS['star']}

{EMOJIS['shop']} <i>Здесь вы можете:</i>
{EMOJIS['check']} Заказать любые товары
{EMOJIS['check']} Получить консультацию
{EMOJIS['check']} Узнать о скидках и акциях
{EMOJIS['check']} Оформить доставку

{EMOJIS['bell']} <b>Как сделать заказ:</b>
1. {EMOJIS['point_right']} Опишите что хотите заказать
2. {EMOJIS['point_right']} Укажите количество и цвет
3. {EMOJIS['point_right']} Напишите адрес доставки
4. {EMOJIS['point_right']} Мы свяжемся с вами!

{EMOJIS['fire']} <b>Горячая линия:</b> 24/7
{EMOJIS['gift']} <b>Бонусы новым клиентам:</b> +10% скидка
{EMOJIS['shield']} <b>Гарантия качества:</b> 100%

{EMOJIS['heart']} <i>Спасибо, что выбрали нас!</i> {EMOJIS['heart']}"""

def format_admin_notification(user_data, message_text, message_type="text"):
    timestamp = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    
    if message_type == "text":
        message_icon = EMOJIS['message']
    else:
        message_icon = EMOJIS['photo']
    
    return f"""{EMOJIS['bell']} <b>НОВЫЙ ЗАПРОС ОТ КЛИЕНТА!</b> {EMOJIS['bell']}

{EMOJIS['user']} <b>Клиент:</b>
{EMOJIS['id']} ID: <code>{user_data['user_id']}</code>
{EMOJIS['user']} Имя: {user_data['user_full_name']}
{EMOJIS['user']} @{user_data['username']}

{message_icon} <b>Сообщение:</b>
<blockquote expandable>{message_text}</blockquote>

{EMOJIS['time']} <b>Время:</b> {timestamp}
{EMOJIS['new']} <b>Статус:</b> Ожидает ответа

{EMOJIS['point_down']} <i>Нажмите кнопку ниже для ответа</i> {EMOJIS['point_down']}"""

def format_reply_notification(user_data):
    return f"""{EMOJIS['reply']} <b>ОТВЕТ НА СООБЩЕНИЕ</b> {EMOJIS['reply']}

{EMOJIS['admin']} <b>Вы отвечаете клиенту:</b>
{EMOJIS['user']} {user_data['user_full_name']}
{EMOJIS['user']} @{user_data['username']}
{EMOJIS['id']} ID: <code>{user_data['user_id']}</code>

{EMOJIS['message']} <b>Исходное сообщение:</b>
<blockquote expandable>{user_data['text'][:150]}...</blockquote>

{EMOJIS['point_down']} <b>Введите ваш ответ ниже:</b> {EMOJIS['point_down']}

{EMOJIS['info']} <i>Можно отправить текст или фото с описанием</i>"""

def format_admin_reply_to_user(admin_message):
    return f"""{EMOJIS['bell']} <b>ОТВЕТ ОТ АДМИНИСТРАТОРА</b> {EMOJIS['bell']}

{EMOJIS['admin']} <b>Администратор магазина:</b>
{EMOJIS['check']} Ответил на ваш запрос
{EMOJIS['time']} Время: {datetime.datetime.now().strftime("%H:%M")}

{EMOJIS['message']} <b>Сообщение:</b>
<blockquote expandable>{admin_message}</blockquote>

{EMOJIS['heart']} <i>Спасибо за обращение! Мы всегда рады помочь!</i>

{EMOJIS['phone']} <b>Телефон поддержки:</b> +7 (XXX) XXX-XX-XX
{EMOJIS['email']} <b>Email:</b> support@shop.ru
{EMOJIS['clock']} <b>Режим работы:</b> 9:00 - 21:00

{EMOJIS['star']} <i>Хорошего дня!</i> {EMOJIS['star']}"""

def format_user_confirmation():
    return f"""{EMOJIS['success']} <b>ВАШ ЗАПРОС ПРИНЯТ!</b> {EMOJIS['success']}

{EMOJIS['check']} Сообщение отправлено администратору
{EMOJIS['check']} Ожидайте ответ в ближайшее время
{EMOJIS['check']} Среднее время ответа: 5-15 минут

{EMOJIS['info']} <b>Что дальше?</b>
1. {EMOJIS['point_right']} Администратор уточнит детали
2. {EMOJIS['point_right']} Рассчитает стоимость заказа
3. {EMOJIS['point_right']} Предложит варианты доставки
4. {EMOJIS['point_right']} Отправит реквизиты для оплаты

{EMOJIS['fire']} <b>Горячая линия:</b> Если нужна срочная помощь
{EMOJIS['gift']} <b>Бонус:</b> При первом заказе +10% скидка!

{EMOJIS['heart']} <i>Спасибо за выбор нашего магазина!</i>"""

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    welcome_text = format_welcome()
    
    # Красивые кнопки
    keyboard = [
        [
            InlineKeyboardButton(f"{EMOJIS['shop']} Каталог", callback_data="catalog"),
            InlineKeyboardButton(f"{EMOJIS['gift']} Акции", callback_data="promo")
        ],
        [
            InlineKeyboardButton(f"{EMOJIS['phone']} Контакты", callback_data="contacts"),
            InlineKeyboardButton(f"{EMOJIS['delivery']} Доставка", callback_data="delivery")
        ],
        [
            InlineKeyboardButton(f"{EMOJIS['money']} Оплата", callback_data="payment"),
            InlineKeyboardButton(f"{EMOJIS['shield']} Гарантии", callback_data="guarantee")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_text,
        parse_mode='HTML',
        reply_markup=reply_markup
    )

# Обработка текстовых сообщений от пользователей
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message_text = update.message.text
    
    # Если пишет администратор
    if user.id == ADMIN_ID:
        # Проверяем, отвечает ли он на сообщение
        if 'replying_to' in context.user_data:
            target_user_id = context.user_data['replying_to']
            target_message_id = context.user_data.get('replying_to_message')
            
            try:
                # Отправляем красивый ответ пользователю
                formatted_reply = format_admin_reply_to_user(message_text)
                
                await context.bot.send_message(
                    chat_id=target_user_id,
                    text=formatted_reply,
                    parse_mode='HTML'
                )
                
                # Подтверждение администратору
                await update.message.reply_text(
                    f"{EMOJIS['success']} <b>ОТВЕТ ОТПРАВЛЕН!</b> {EMOJIS['success']}\n\n"
                    f"{EMOJIS['check']} Клиент получил ваше сообщение\n"
                    f"{EMOJIS['check']} Сообщение доставлено успешно\n"
                    f"{EMOJIS['clock']} Время: {datetime.datetime.now().strftime('%H:%M:%S')}",
                    parse_mode='HTML'
                )
                
                # Удаляем сообщение из хранилища
                if target_message_id in user_messages:
                    del user_messages[target_message_id]
                
                # Очищаем состояние ответа
                context.user_data.pop('replying_to', None)
                context.user_data.pop('replying_to_message', None)
                
            except Exception as e:
                await update.message.reply_text(
                    f"{EMOJIS['error']} <b>ОШИБКА ОТПРАВКИ!</b> {EMOJIS['error']}\n\n"
                    f"{EMOJIS['warning']} Не удалось отправить сообщение\n"
                    f"{EMOJIS['info']} Ошибка: {str(e)[:100]}",
                    parse_mode='HTML'
                )
        return
    
    # Сохраняем сообщение от обычного пользователя
    message_id = update.message.message_id
    user_messages[message_id] = {
        'user_id': user.id,
        'username': user.username or user.first_name,
        'user_full_name': f"{user.first_name} {user.last_name or ''}",
        'text': message_text,
        'chat_id': update.message.chat_id,
        'timestamp': datetime.datetime.now()
    }
    
    # Форматируем уведомление для администратора
    admin_notification = format_admin_notification(user_messages[message_id], message_text)
    
    # Кнопка для ответа
    keyboard = [[
        InlineKeyboardButton(
            f"{EMOJIS['reply']} Ответить клиенту", 
            callback_data=f"reply_{message_id}"
        )
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        # Отправляем уведомление администратору
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=admin_notification,
            parse_mode='HTML',
            reply_markup=reply_markup
        )
        
        # Подтверждение пользователю
        user_confirmation = format_user_confirmation()
        await update.message.reply_text(
            user_confirmation,
            parse_mode='HTML'
        )
        
    except Exception as e:
        await update.message.reply_text(
            f"{EMOJIS['error']} Произошла ошибка при отправке сообщения.",
            parse_mode='HTML'
        )

# Обработка фото с текстом
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    caption = update.message.caption or "Фото без описания"
    photo = update.message.photo[-1]
    
    # Если пишет администратор
    if user.id == ADMIN_ID:
        if 'replying_to' in context.user_data:
            target_user_id = context.user_data['replying_to']
            target_message_id = context.user_data.get('replying_to_message')
            
            try:
                # Отправляем фото с красивым текстом
                formatted_reply = format_admin_reply_to_user(caption)
                
                await context.bot.send_photo(
                    chat_id=target_user_id,
                    photo=photo.file_id,
                    caption=formatted_reply,
                    parse_mode='HTML'
                )
                
                # Подтверждение администратору
                await update.message.reply_text(
                    f"{EMOJIS['success']} <b>ФОТО ОТПРАВЛЕНО!</b> {EMOJIS['success']}\n\n"
                    f"{EMOJIS['check']} Клиент получил ваше фото\n"
                    f"{EMOJIS['check']} Сообщение доставлено успешно",
                    parse_mode='HTML'
                )
                
                # Удаляем сообщение из хранилища
                if target_message_id in user_messages:
                    del user_messages[target_message_id]
                
                # Очищаем состояние ответа
                context.user_data.pop('replying_to', None)
                context.user_data.pop('replying_to_message', None)
                
            except Exception as e:
                await update.message.reply_text(
                    f"{EMOJIS['error']} <b>ОШИБКА ОТПРАВКИ ФОТО!</b>\n\n{str(e)[:100]}",
                    parse_mode='HTML'
                )
        return
    
    # Сохраняем сообщение с фото от обычного пользователя
    message_id = update.message.message_id
    user_messages[message_id] = {
        'user_id': user.id,
        'username': user.username or user.first_name,
        'user_full_name': f"{user.first_name} {user.last_name or ''}",
        'text': caption,
        'photo_id': photo.file_id,
        'chat_id': update.message.chat_id,
        'timestamp': datetime.datetime.now()
    }
    
    # Форматируем уведомление для администратора
    admin_notification = format_admin_notification(user_messages[message_id], caption, "photo")
    
    # Кнопка для ответа
    keyboard = [[
        InlineKeyboardButton(
            f"{EMOJIS['reply']} Ответить клиенту", 
            callback_data=f"reply_{message_id}"
        )
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        # Отправляем фото администратору
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo.file_id,
            caption=admin_notification,
            parse_mode='HTML',
            reply_markup=reply_markup
        )
        
        # Подтверждение пользователю
        user_confirmation = format_user_confirmation()
        await update.message.reply_text(
            user_confirmation,
            parse_mode='HTML'
        )
        
    except Exception as e:
        await update.message.reply_text(
            f"{EMOJIS['error']} Произошла ошибка при отправке фото.",
            parse_mode='HTML'
        )

# Обработка нажатия кнопок
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    
    try:
        await query.answer()
    except:
        pass
    
    data = query.data
    
    if data.startswith("reply_"):
        try:
            message_id = int(data.split("_")[1])
            
            if message_id in user_messages:
                user_data = user_messages[message_id]
                
                # Сохраняем ID пользователя для ответа
                context.user_data['replying_to'] = user_data['user_id']
                context.user_data['replying_to_message'] = message_id
                
                # Форматируем сообщение о начале ответа
                reply_notification = format_reply_notification(user_data)
                
                await query.edit_message_text(
                    text=reply_notification,
                    parse_mode='HTML'
                )
            else:
                await query.edit_message_text(
                    f"{EMOJIS['error']} <b>СООБЩЕНИЕ УСТАРЕЛО</b>\n\n"
                    f"{EMOJIS['warning']} Это сообщение было удалено или обработано ранее.",
                    parse_mode='HTML'
                )
        except Exception as e:
            logger.error(f"Error in button_callback: {e}")
            await query.message.reply_text(
                f"{EMOJIS['error']} Произошла ошибка при обработке запроса.",
                parse_mode='HTML'
            )
    
    # Обработка других кнопок
    elif data == "catalog":
        await query.edit_message_text(
            f"{EMOJIS['shop']} <b>НАШ КАТАЛОГ</b> {EMOJIS['shop']}\n\n"
            f"{EMOJIS['check']} <b>Электроника:</b> Телефоны, ноутбуки, планшеты\n"
            f"{EMOJIS['check']} <b>Бытовая техника:</b> Холодильники, стиральные машины\n"
            f"{EMOJIS['check']} <b>Одежда:</b> Мужская, женская, детская\n"
            f"{EMOJIS['check']} <b>Красота и здоровье:</b> Косметика, парфюмерия\n"
            f"{EMOJIS['check']} <b>Спорт:</b> Одежда, инвентарь, питание\n\n"
            f"{EMOJIS['point_right']} <i>Напишите что хотите заказать!</i>",
            parse_mode='HTML'
        )
    elif data == "promo":
        await query.edit_message_text(
            f"{EMOJIS['gift']} <b>АКЦИИ И СКИДКИ</b> {EMOJIS['gift']}\n\n"
            f"{EMOJIS['fire']} <b>ГОРЯЧИЕ ПРЕДЛОЖЕНИЯ:</b>\n"
            f"{EMOJIS['discount']} <b>Скидка 20%</b> на первый заказ\n"
            f"{EMOJIS['discount']} <b>2+1 бесплатно</b> на косметику\n"
            f"{EMOJIS['discount']} <b>Бесплатная доставка</b> от 5000₽\n"
            f"{EMOJIS['discount']} <b>Подарок</b> при заказе от 10000₽\n\n"
            f"{EMOJIS['star']} <i>Успейте воспользоваться!</i>",
            parse_mode='HTML'
        )
    elif data == "contacts":
        await query.edit_message_text(
            f"{EMOJIS['phone']} <b>НАШИ КОНТАКТЫ</b> {EMOJIS['phone']}\n\n"
            f"{EMOJIS['phone']} <b>Телефон:</b> +7 (XXX) XXX-XX-XX\n"
            f"{EMOJIS['email']} <b>Email:</b> info@shop.ru\n"
            f"{EMOJIS['location']} <b>Адрес:</b> г. Москва, ул. Примерная, 1\n"
            f"{EMOJIS['clock']} <b>Режим работы:</b> 9:00 - 21:00\n\n"
            f"{EMOJIS['heart']} <i>Ждем ваших обращений!</i>",
            parse_mode='HTML'
        )
    elif data == "delivery":
        await query.edit_message_text(
            f"{EMOJIS['delivery']} <b>УСЛОВИЯ ДОСТАВКИ</b> {EMOJIS['delivery']}\n\n"
            f"{EMOJIS['check']} <b>Курьерская доставка:</b> 1-3 дня, от 300₽\n"
            f"{EMOJIS['check']} <b>Самовывоз:</b> Бесплатно, 25 пунктов\n"
            f"{EMOJIS['check']} <b>Почта России:</b> 5-14 дней, от 200₽\n"
            f"{EMOJIS['check']} <b>Экспресс-доставка:</b> В день заказа, 500₽\n\n"
            f"{EMOJIS['info']} <i>Подробности уточняйте у менеджера</i>",
            parse_mode='HTML'
        )
    elif data == "payment":
        await query.edit_message_text(
            f"{EMOJIS['money']} <b>СПОСОБЫ ОПЛАТЫ</b> {EMOJIS['money']}\n\n"
            f"{EMOJIS['credit_card']} <b>Банковской картой:</b> Visa, MasterCard, МИР\n"
            f"{EMOJIS['bank']} <b>Онлайн-банкинг:</b> Сбербанк, Тинькофф, Альфа\n"
            f"{EMOJIS['money']} <b>Наличными:</b> Курьеру или в пункте выдачи\n"
            f"{EMOJIS['credit_card']} <b>Рассрочка:</b> 0-0-24 от Тинькофф\n\n"
            f"{EMOJIS['shield']} <i>Все платежи защищены!</i>",
            parse_mode='HTML'
        )
    elif data == "guarantee":
        await query.edit_message_text(
            f"{EMOJIS['shield']} <b>НАШИ ГАРАНТИИ</b> {EMOJIS['shield']}\n\n"
            f"{EMOJIS['check']} <b>Гарантия качества:</b> 100% оригинальные товары\n"
            f"{EMOJIS['check']} <b>Возврат:</b> 14 дней без вопросов\n"
            f"{EMOJIS['check']} <b>Обмен:</b> В течение 30 дней\n"
            f"{EMOJIS['check']} <b>Конфиденциальность:</b> Данные защищены\n"
            f"{EMOJIS['check']} <b>Поддержка:</b> 24/7 по телефону и чату\n\n"
            f"{EMOJIS['star']} <i>Мы гарантируем ваш комфорт!</i>",
            parse_mode='HTML'
        )

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = f"""{EMOJIS['info']} <b>ПОМОЩЬ ПО ИСПОЛЬЗОВАНИЮ БОТА</b> {EMOJIS['info']}

{EMOJIS['check']} <b>Как сделать заказ:</b>
{EMOJIS['point_right']} Напишите что хотите заказать
{EMOJIS['point_right']} Укажите количество и характеристики
{EMOJIS['point_right']} Опишите адрес доставки
{EMOJIS['point_right']} Дождитесь ответа менеджера

{EMOJIS['check']} <b>Доступные команды:</b>
{EMOJIS['check']} /start - Главное меню
{EMOJIS['check']} /help - Эта справка
{EMOJIS['check']} /status - Статус заказов

{EMOJIS['check']} <b>Примеры сообщений:</b>
{EMOJIS['message']} "Хочу заказать iPhone 15 Pro 256GB черный"
{EMOJIS['message']} "Нужны кроссовки Nike размер 42, 2 пары"
{EMOJIS['message']} "Интересует доставка холодильника в Казань"

{EMOJIS['fire']} <b>Срочная помощь:</b>
{EMOJIS['phone']} Телефон: +7 (XXX) XXX-XX-XX
{EMOJIS['clock']} Круглосуточно, без выходных

{EMOJIS['heart']} <i>Мы всегда рады помочь!</i>"""
    
    await update.message.reply_text(help_text, parse_mode='HTML')

# Команда /status
async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    if user.id == ADMIN_ID:
        # Статистика для администратора
        active_orders = len(user_messages)
        
        status_text = f"""{EMOJIS['settings']} <b>СТАТИСТИКА СИСТЕМЫ</b> {EMOJIS['settings']}

{EMOJIS['bell']} <b>Текущая активность:</b>
{EMOJIS['order']} Активных заказов: <b>{active_orders}</b>
{EMOJIS['user']} Уникальных клиентов: <b>{len(set(msg['user_id'] for msg in user_messages.values()))}</b>
{EMOJIS['time']} Время сервера: {datetime.datetime.now().strftime('%H:%M:%S')}

{EMOJIS['check']} <b>Статус бота:</b> Работает нормально
{EMOJIS['check']} <b>Скорость ответа:</b> Мгновенная
{EMOJIS['check']} <b>Ошибок:</b> Нет

{EMOJIS['star']} <i>Все системы функционируют стабильно!</i>"""
    else:
        # Информация для пользователя
        status_text = f"""{EMOJIS['clock']} <b>СТАТУС ВАШИХ ЗАКАЗОВ</b> {EMOJIS['clock']}

{EMOJIS['check']} <b>Система уведомлений:</b> Активна
{EMOJIS['check']} <b>Поддержка онлайн:</b> Да
{EMOJIS['check']} <b>Время ответа:</b> 5-15 минут

{EMOJIS['info']} <b>Если вы отправили заказ:</b>
{EMOJIS['green_circle']} Он получен администратором
{EMOJIS['yellow_circle']} Находится в обработке
{EMOJIS['green_circle']} Вам скоро ответят

{EMOJIS['warning']} <b>Если ответа нет долго:</b>
{EMOJIS['phone']} Позвоните: +7 (XXX) XXX-XX-XX
{EMOJIS['bell']} Напишите еще раз в чат

{EMOJIS['heart']} <i>Спасибо за ожидание!</i>"""
    
    await update.message.reply_text(status_text, parse_mode='HTML')

# Главная функция
def main():
    # Создание приложения
    application = Application.builder().token(TOKEN).build()
    
    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    
    # Обработчик кнопок
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Обработчики сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    # Запуск бота с красивым приветствием
    print("=" * 60)
    print(f"{EMOJIS['rocket']}  БОТ УСПЕШНО ЗАПУЩЕН!  {EMOJIS['rocket']}")
    print("=" * 60)
    print(f"{EMOJIS['admin']}  Администратор: ID {ADMIN_ID}")
    print(f"{EMOJIS['time']}  Время запуска: {datetime.datetime.now().strftime('%H:%M:%S')}")
    print(f"{EMOJIS['check']}  Статус: Ожидание сообщений...")
    print(f"{EMOJIS['star']}  Бот готов к работе!")
    print("=" * 60)
    
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )

if __name__ == '__main__':
    main()