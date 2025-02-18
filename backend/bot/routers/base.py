from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, Message, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import WEBAPP_URL

router = Router()

START_MESSAGE = '🤖 Hello from telegram bot\nYou can test mini app by clicking the button'

@router.message(CommandStart())
async def start(message: Message):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='Open 👀', web_app=WebAppInfo(url=WEBAPP_URL))
    )

    await message.answer(START_MESSAGE, reply_markup=builder.as_markup())