from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def register_start(dp):
    @dp.message_handler(commands=['start'])
    async def start_cmd(message: types.Message):
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("➕ Add Account", callback_data="add_account")],
            [InlineKeyboardButton("📧 Add SMTP", callback_data="add_smtp")],
            [InlineKeyboardButton("🚨 Report", callback_data="report")],
            [InlineKeyboardButton("👤 Owner", callback_data="owner")],
        ])
        await message.answer("Welcome! What do you want to do?", reply_markup=kb)
