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

TOKEN = '6530479075:AAHvVqTaxfqtnbr4DO3XJaPfIodTZ6Tp9sU'
bot = Bot(TOKEN)
dp = Dispatcher()

admin_id=[1230922952, 1381182544, 1091393092]
#admin_id=[1230922952]

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if message.from_user.id in admin_id:
        await message.answer(f"Вітаю *Адміністратору* *{message.from_user.full_name}*!\n\nСюди ти можеш надіслати контент для адмінів 🥰", parse_mode='Markdown')
    else:
        await message.answer(f"Вітаю, *{message.from_user.full_name}*!\n\nСюди ти можеш надіслати контент для адмінів 🥰", parse_mode='Markdown')

@dp.message()
async def echo_handler(message: Message) -> None:
    if message.from_user.id in banned_users:
        await message.reply("You are banned from sending messages.")
    else:
        try:
            for group_id in admin_id:
                await bot.forward_message(chat_id=group_id, from_chat_id=message.chat.id, message_id=message.message_id)
                #await bot.send_message(chat_id=group_id, text=f"author: @{message.from_user.username}" "\nID = " f"{message.from_user.id}")
                await bot.send_message(chat_id=group_id, text=f"author: @{message.from_user.username}")
            await message.reply("Ваше повідомлення було надіслано адміністраторам ❤️", parse_mode='Markdown')
    
        except TypeError:
            await message.answer("Помилка")    

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())