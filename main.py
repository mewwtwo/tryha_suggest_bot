import asyncio,logging,sys
from os import getenv
from keep_alive import keep_alive
keep_alive()
from aiogram import Bot, Dispatcher, html, types
from aiogram.methods.forward_message import ForwardMessage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

#TOKEN='6991919463:AAFRs2jw5aeQ7rVSErljwFYNlD1ev0_eMmg'
TOKEN = '6530479075:AAHvVqTaxfqtnbr4DO3XJaPfIodTZ6Tp9sU'
bot = Bot(TOKEN)
dp = Dispatcher()
#admin_id=[1230922952]
admin_id=[1230922952, 1381182544, 1091393092]
banned_users = []

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if message.from_user.id in admin_id:
        await message.answer(f"Вітаю *Адміністратору* *{message.from_user.full_name}*!\n\nСюди ти можеш надіслати контент 🥰\n\help - інструкція по використанню", parse_mode='Markdown')
    else:
        await message.answer(f"Вітаю, *{message.from_user.full_name}*!\n\nСюди ти можеш надіслати контент для адмінів 🥰", parse_mode='Markdown')
        
@dp.message(Command('ban'))
async def ban_user(message: Message):
    try:
        command, user_id_str = message.text.split(maxsplit=1)
        user_id = int(user_id_str)
        
        if user_id not in banned_users:
            banned_users.append(user_id)
            await message.reply(f"Користувача {user_id} було заблоковано 🎉")
        else:
            
            
            await message.reply(f"Користувач {user_id} вже заблокований 😄")
    except (ValueError, IndexError):
            
        await message.reply("❗️Використовуйте формат '/ban 123456789'")

@dp.message(Command('unban'))
async def ban_user(message: Message):
    try:
        command, user_id_str = message.text.split(maxsplit=1)
        user_id = int(user_id_str)
        
        if user_id in banned_users:
            banned_users.remove(user_id)
            await message.reply(f"Користувача {user_id} було розблоковано 🎉")
        else:
            
            
            await message.reply(f"Користувач {user_id} вже розблокований 😄")
    except (ValueError, IndexError):
        await message.reply("❗️Використовуйте формат '/unban 123456789'")

@dp.message(Command('send'))
async def send_message(message: Message):
    try:
        if message.from_user.id in admin_id:
            command, user_id_str, text = message.text.split(maxsplit=2)
            user_id = int(user_id_str)
            await bot.send_message(chat_id=user_id, text=text)
            await message.reply(f"Повідомлення було відправлено для 😘 {user_id}: {text}")
    except (ValueError, IndexError):
        await message.reply("❗️Використовуйте формат '/send 123456789 ваше повідомлення'")
        
@dp.message(Command('help'))
async def help(message: Message):
    if message.from_user.id in admin_id:
        await message.answer(f"Вітаю *Адміністратору* *{message.from_user.full_name}*!\nОсь тобі коротенька інструкція, як працювати з цим ботом 🤓\n\n/ban 123456789 - заблокувати користувача (буде в списку до рестарта бота)\n/unban 123456789 - розблокувати користувача\n/send 123456789 повідомлення - надіслати повідомлення для користувача", parse_mode='Markdown')
    else:
        await message.answer(f"Вітаю, *{message.from_user.full_name}*!\n\nСюди ти можеш надіслати контент для адмінів 🥰", parse_mode='Markdown')
    
@dp.message()
async def handler(message: Message) -> None:
    if message.from_user.id in banned_users:
        await message.reply("Ви більше не можете надсилати повідомлення 😓")  
    else:
        if message.from_user.id not in admin_id:
            try:
                for group_id in admin_id:
                    await bot.forward_message(chat_id=group_id, from_chat_id=message.chat.id, message_id=message.message_id)
                    await bot.send_message(chat_id=group_id, text=f"👤 автор: @{message.from_user.username}" "\nID = " f"{message.from_user.id}")
                    #await bot.send_message(chat_id=group_id, text=f"author: @{message.from_user.username}")
                await message.reply("Ваше повідомлення було надіслано адміністраторам ❤️", parse_mode='Markdown')
            except TypeError:
                await message.answer("Помилка 😓")   
        else:
            try:
                for group_id in admin_id:
                    await bot.forward_message(chat_id=group_id, from_chat_id=message.chat.id, message_id=message.message_id)
                    await bot.send_message(chat_id=group_id, text=f"від адміна: @{message.from_user.username}")
            except TypeError:
                await message.answer("Помилка 😓")  
        

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())