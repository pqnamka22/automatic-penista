from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
from aiogram.utils import executor

bot = Bot(token="8168424922:AAEi0QOsZ4iX9K0e7JiU1PiRqlIZIaXb4sc")
dp = Dispatcher(bot)

OWNER_ID = 8233512755  # ID владельца бота
owner_replying_to = None  # ID пользователя, которому отвечает владелец
chat_history = {}  # История чатов
waiting_for_message = set()  # Пользователи, ожидающие ответа

def owner_reply_kb(user_id):
    # Клавиатура для владельца для ответа пользователю
    return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text="Ответить", callback_data=f"reply_{user_id}")
    )

@dp.message_handler(content_types=[ContentType.TEXT, ContentType.PHOTO, ContentType.VIDEO, ContentType.VIDEO_NOTE])
async def message_handler(message: types.Message):
    global owner_replying_to
    user_id = message.from_user.id

    # Если сообщение от владельца и он отвечает конкретному пользователю
    if user_id == OWNER_ID:
        if owner_replying_to:
            to_user = owner_replying_to
            # Отправляем текст без других медиа
            if message.text and not (message.photo or message.video or message.video_note):
                await bot.send_message(to_user, message.text)
                chat_history.setdefault(to_user, []).append({"from": "owner", "type": "text", "content": message.text})

            # Фото с подписью
            if message.photo:
                photo = message.photo[-1]
                caption = message.caption or ""
                await bot.send_photo(to_user, photo.file_id, caption=caption)
                chat_history.setdefault(to_user, []).append({"from": "owner", "type": "photo", "content": photo.file_id, "caption": caption})

            # Видео с подписью
            if message.video:
                video = message.video
                caption = message.caption or ""
                await bot.send_video(to_user, video.file_id, caption=caption)
                chat_history.setdefault(to_user, []).append({"from": "owner", "type": "video", "content": video.file_id, "caption": caption})

            # Видео-кружок (video_note) без подписи
            if message.video_note:
                video_note = message.video_note
                await bot.send_video_note(to_user, video_note.file_id)
                chat_history.setdefault(to_user, []).append({"from": "owner", "type": "video_note", "content": video_note.file_id})

    else:
        # Сообщение от пользователя — сохраняем и пересылаем владельцу
        if message.text:
            chat_history.setdefault(user_id, []).append({"from": "user", "type": "text", "content": message.text})
            await bot.send_message(OWNER_ID, f"Сообщение от {user_id}: {message.text}", reply_markup=owner_reply_kb(user_id))

        elif message.photo:
            photo = message.photo[-1]
            caption = message.caption or ""
            chat_history.setdefault(user_id, []).append({"from": "user", "type": "photo", "content": photo.file_id, "caption": caption})
            await bot.send_photo(OWNER_ID, photo.file_id, caption=f"От пользователя {user_id}\n{caption}", reply_markup=owner_reply_kb(user_id))

        elif message.video:
            video = message.video
            caption = message.caption or ""
            chat_history.setdefault(user_id, []).append({"from": "user", "type": "video", "content": video.file_id, "caption": caption})
            await bot.send_video(OWNER_ID, video.file_id, caption=f"От пользователя {user_id}\n{caption}", reply_markup=owner_reply_kb(user_id))

        elif message.video_note:
            video_note = message.video_note
            chat_history.setdefault(user_id, []).append({"from": "user", "type": "video_note", "content": video_note.file_id})
            await bot.send_video_note(OWNER_ID, video_note.file_id, reply_markup=owner_reply_kb(user_id))

if name == "__main__":
    executor.start_polling(dp)
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
from aiogram.utils import executor

bot = Bot(token="8168424922:AAEi0QOsZ4iX9K0e7JiU1PiRqlIZIaXb4sc")
dp = Dispatcher(bot)

OWNER_ID = 8233512755  # ID владельца бота
owner_replying_to = None  # ID пользователя, которому отвечает владелец
chat_history = {}  # История чатов
waiting_for_message = set()  # Пользователи, ожидающие ответа

def owner_reply_kb(user_id):
    # Клавиатура для владельца для ответа пользователю
    return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text="Ответить", callback_data=f"reply_{user_id}")
    )

@dp.message_handler(content_types=[ContentType.TEXT, ContentType.PHOTO, ContentType.VIDEO, ContentType.VIDEO_NOTE])
async def message_handler(message: types.Message):
    global owner_replying_to
    user_id = message.from_user.id

    # Если сообщение от владельца и он отвечает конкретному пользователю
    if user_id == OWNER_ID:
        if owner_replying_to:
            to_user = owner_replying_to
            # Отправляем текст без других медиа
            if message.text and not (message.photo or message.video or message.video_note):
                await bot.send_message(to_user, message.text)
                chat_history.setdefault(to_user, []).append({"from": "owner", "type": "text", "content": message.text})

            # Фото с подписью
            if message.photo:
                photo = message.photo[-1]
                caption = message.caption or ""
                await bot.send_photo(to_user, photo.file_id, caption=caption)
                chat_history.setdefault(to_user, []).append({"from": "owner", "type": "photo", "content": photo.file_id, "caption": caption})

            # Видео с подписью
            if message.video:
                video = message.video
                caption = message.caption or ""
                await bot.send_video(to_user, video.file_id, caption=caption)
                chat_history.setdefault(to_user, []).append({"from": "owner", "type": "video", "content": video.file_id, "caption": caption})

            # Видео-кружок (video_note) без подписи
            if message.video_note:
                video_note = message.video_note
                await bot.send_video_note(to_user, video_note.file_id)
                chat_history.setdefault(to_user, []).append({"from": "owner", "type": "video_note", "content": video_note.file_id})

    else:
        # Сообщение от пользователя — сохраняем и пересылаем владельцу
        if message.text:
            chat_history.setdefault(user_id, []).append({"from": "user", "type": "text", "content": message.text})
            await bot.send_message(OWNER_ID, f"Сообщение от {user_id}: {message.text}", reply_markup=owner_reply_kb(user_id))

        elif message.photo:
            photo = message.photo[-1]
            caption = message.caption or ""
            chat_history.setdefault(user_id, []).append({"from": "user", "type": "photo", "content": photo.file_id, "caption": caption})
            await bot.send_photo(OWNER_ID, photo.file_id, caption=f"От пользователя {user_id}\n{caption}", reply_markup=owner_reply_kb(user_id))

        elif message.video:
            video = message.video
            caption = message.caption or ""
            chat_history.setdefault(user_id, []).append({"from": "user", "type": "video", "content": video.file_id, "caption": caption})
            await bot.send_video(OWNER_ID, video.file_id, caption=f"От пользователя {user_id}\n{caption}", reply_markup=owner_reply_kb(user_id))

        elif message.video_note:
            video_note = message.video_note
            chat_history.setdefault(user_id, []).append({"from": "user", "type": "video_note", "content": video_note.file_id})
            await bot.send_video_note(OWNER_ID, video_note.file_id, reply_markup=owner_reply_kb(user_id))

if name == "__main__":
    executor.start_polling(dp)
    
