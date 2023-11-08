import os
import random

from dotenv import load_dotenv


load_dotenv()
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")


import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram import F

# Bot token can be obtained via https://t.me/BotFather

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


class MyCallback(CallbackData, prefix="my"):
    press_data: str


@dp.message(Command("buttons"))
async def command_buttons_handler(message: Message) -> None:
    """
    This handler receives messages with `/buttons` command

    https://docs.aiogram.dev/en/dev-3.x/dispatcher/filters/callback_data.html
    """
    # CallbackData is a helper class to create CallbackQuery data

    cb_press = MyCallback(press_data="press")
    cb_dont_press = MyCallback(press_data="dont_press")
    cb_press_too = MyCallback(press_data="press_too")
    print(cb_press.pack())
    print(cb_dont_press.pack())
    print(cb_press_too.pack())

    await message.answer(
        "Here are your buttons:",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(text="Press me", callback_data=cb_press.pack()),
                    types.InlineKeyboardButton(text="Don't press me", callback_data=cb_dont_press.pack()),
                ],
                [types.InlineKeyboardButton(text="Press me too", callback_data=cb_press_too.pack())],
            ],
        ),
    )


@dp.callback_query(MyCallback.filter(F.press_data=="press"))
async def callback_press_handler(query: types.CallbackQuery, callback_data: dict[str, str]) -> None:
    """
    This handler receives callback queries with `press` field equal to `True`
    """
    await query.message.edit_text("You pressed the button!")
    await query.answer("You pressed the button!", show_alert=True)


@dp.callback_query(MyCallback.filter(F.press_data=="dont_press"))
async def callback_dont_press_handler(query: types.CallbackQuery, callback_data: dict[str, str]) -> None:
    """
    This handler receives callback queries with `dont_press` field equal to `True`
    """
    await query.message.edit_text("You shouldn't have pressed that button!")
    await query.answer("You shouldn't have pressed that button!", show_alert=True)


@dp.callback_query(MyCallback.filter(F.press_data=="press_too"))
async def callback_press_too_handler(query: types.CallbackQuery, callback_data: dict[str, str]) -> None:
    """
    This handler receives callback queries with `press_too` field equal to `True`
    """
    await query.message.edit_text("You pressed the button too!")
    await query.answer("You pressed the button too!", show_alert=True)



async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TG_BOT_TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

