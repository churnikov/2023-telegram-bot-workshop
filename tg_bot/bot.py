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
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.types.keyboard_button import KeyboardButton
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup

# Bot token can be obtained via https://t.me/BotFather

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()

class Game:
    def __init__(self):
        self.reset()

    def guess(self, number):
        if self.guesses >= self.max_guesses:
            return f"You have no more guesses left. The number was {self.number}"
        self.guesses += 1
        if number == self.number:
            return "You guessed it!"
        elif number < self.number:
            self.current_min = number + 1
            return "Too low"
        else:
            self.current_max = number - 1
            return "Too high"

    def reset(self):
        self.number = random.randint(1, 100)
        self.guesses = 0
        self.max_guesses = 10
        self.current_min = 1
        self.current_max = 100

def update_buttons(min_num, max_num):
    buttons = []

    step = (max_num - min_num) // 9
    for i in range(10):
        guess = min_num + i * step
        button = KeyboardButton(text=str(guess))
        buttons.append(button)
    return ReplyKeyboardMarkup(keyboard=[buttons],
            resize_keyboard=True)


db = {}


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
    db[message.from_user.id] = Game()
    await message.answer("I'm thinking of a number between 1 and 100. You have 10 guesses",
                         reply_markup=update_buttons(1, 100))



@dp.message(Command("reset"))
async def command_reset_handler(message: Message) -> None:
    """
    This handler receives messages with `/reset` command
    """
    if message.from_user.id not in db:
        await message.answer("Start a game first")
        return
    game = db[message.from_user.id]
    game.reset()
    await message.answer("Game reset")
    await message.answer("I'm thinking of a number between 1 and 100. You have 10 guesses",
                         reply_markup=update_buttons(1, 100))


@dp.message()
async def handle_guess(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    if message.from_user.id not in db:
        await message.answer("Start a game first")
        return
    game = db[message.from_user.id]
    try:
        guess = int(message.text)
    except ValueError:
        await message.answer("Please, enter a number")
        return
    resp = game.guess(guess)
    kbrd = update_buttons(game.current_min, game.current_max)
    await message.answer(resp, reply_markup=kbrd)
    if game.guesses >= game.max_guesses:
        del db[message.from_user.id]

async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TG_BOT_TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

