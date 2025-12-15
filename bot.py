from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ContentType
from aiogram.utils import executor
import asyncio
from datetime import datetime

TOKEN = "8168424922:AAEi0QOsZ4iX9K0e7JiU1PiRqlIZIaXb4sc"
OWNER_ID = 8233512755  # Ваш Telegram user ID (int)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Храним состояние, кто готов отправлять сообщение
waiting_for_message = set()

# Храним чат: {user_id: [{"from": "user"/"owner", "content": ..., "type": "text"/"photo"}]}
chat_history = {}

# Храним, кому владелец сейчас отвечает
owner_replying_to = None

# Клавиатура с кнопкой "Отправить сооб!"
def main_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Отправить сооб!", callback_data="send_message"))
    return kb

# Клавиатура для владельца с кнопкой ответить
def owner_reply_kb(user_id):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Ответить на сообщение от имени бота", callback_data=f"reply_{user_id}"))
    return kb

# Клавиатура отмены для владельца
def cancel_reply_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("❌ Отменить ответ", callback_data="cancel_reply"))
    return kb

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer("Привет! Нажми на кнопку отправить сооб!", reply_markup=main_kb())
    chat_history.setdefault(message.from_user.id, [])

@dp.callback_query_handler(lambda c: c.data == "send_message")
async def callback_send_message(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    waiting_for_message.add(user_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(user_id, "Кидай сюда все что хочешь увидеть в подслушке @tgk1103")

@dp.callback_query_handler(lambda c: c.data.startswith("reply_"))
async def callbacks_reply(callback_query: types.CallbackQuery):
    global owner_replying_to
    await bot.answer_callback_query(callback_query.id)
    user_id = int(callback_query.data.split("_")[1])
    
    # Запоминаем, кому отвечаем
    owner_replying_to = user_id
    
    # Показываем последние сообщения для контекста
    context_msg = ""
    if user_id in chat_history:
        recent = chat_history[user_id][-5:]
        msg_text = "\n".join(f"{'👤 Пользователь' if m['from']=='user' else '🤖 Бот'}: {m['content']}" for m in recent if m['type']=='text')
        if msg_text:
            context_msg = f"\n\nПоследние сообщения:\n{msg_text}"
    
    await bot.send_message(
        callback_query.from_user.id,
        f"✍️ Режим ответа активирован!\n\nПросто напишите сообщение, и оно будет отправлено пользователю.{context_msg}",
        reply_markup=cancel_reply_kb()
    )

@dp.callback_query_handler(lambda c: c.data == "cancel_reply")
async def callback_cancel_reply(callback_query: types.CallbackQuery):
    global owner_replying_to
    await bot.answer_callback_query(callback_query.id)
    owner_replying_to = None
    await bot.send_message(callback_query.from_user.id, "❌ Режим ответа отменён.")

@dp.message_handler(content_types=[ContentType.TEXT, ContentType.PHOTO])
async def message_handler(message: types.Message):
    global owner_replying_to
    user_id = message.from_user.id

    # Обработка сообщений от владельца (ID=OWNER_ID) для ответов
    if user_id == OWNER_ID:
        if owner_replying_to:
            to_user = owner_replying_to
            # Отправляем ответ пользователю от имени бота
            if message.text:
                await bot.send_message(to_user, message.text)
                chat_history.setdefault(to_user, []).append({"from": "owner", "type": "text", "content": message.text})
            if message.photo:
                photo = message.photo[-1]
                await bot.send_photo(to_user, photo.file_id)
                chat_history.setdefault(to_user, []).append({"from": "owner", "type": "photo", "content": photo.file_id})
            
            # Сбрасываем режим ответа
            owner_replying_to = None
            await message.answer("✅ Ответ отправлен!")
        else:
            await message.answer("Нажмите кнопку «Ответить» под сообщением пользователя, чтобы ответить.")
        return

    # Проверяем, ожидаем ли от пользователя сообщение
    if user_id not in waiting_for_message:
        return  # Игнорируем все, если не нажимали кнопку

    # Сохраняем в историю
    entries = []
    if message.text:
        entries.append({"from": "user", "type": "text", "content": message.text})

    if message.photo:
        # Берём максимальное качество
        photo = message.photo[-1]
        entries.append({"from": "user", "type": "photo", "content": photo.file_id})

    if not entries:
        await message.reply("Пожалуйста, отправьте текст и/или фото.")
        return

    chat_history.setdefault(user_id, []).extend(entries)
    waiting_for_message.discard(user_id)
    await message.reply("Сообщение отправлено!")

    # Формируем уведомление для владельца
    user_name = f"@{message.from_user.username}" if message.from_user.username else message.from_user.full_name
    dt_str = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    intro = f"Новое сообщение!\nОт: {user_name}\nДата, время: {dt_str}"

    # Отправляем текстовое уведомление с кнопкой ответить
    inline_kb = owner_reply_kb(user_id)
    await bot.send_message(OWNER_ID, intro, reply_markup=inline_kb)

    # Перешлём сообщения (текст и фото) владельцу
    for item in entries:
        if item["type"] == "text":
            await bot.send_message(OWNER_ID, item["content"])
        elif item["type"] == "photo":
            await bot.send_photo(OWNER_ID, item["content"], caption="Фото от пользователя")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

