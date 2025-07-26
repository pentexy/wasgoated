from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from storage.utils import load_json
import datetime

user_report_state = {}
SMTP_FILE = 'data/smtp_accounts.json'
ACCOUNTS_FILE = 'data/telegram_accounts.json'
FORMAT_FILE = 'data/report_format.txt'

def register_report(dp):
    @dp.callback_query_handler(lambda c: c.data == 'report')
    async def ask_username(callback_query: types.CallbackQuery):
        await callback_query.message.answer("Enter the @username to report:")
        user_report_state[callback_query.from_user.id] = {'state': 'awaiting_username'}

    @dp.message_handler(lambda message: user_report_state.get(message.from_user.id, {}).get('state') == 'awaiting_username')
    async def get_times(message: types.Message):
        user_report_state[message.from_user.id] = {
            'state': 'awaiting_count',
            'username': message.text.strip()
        }
        await message.answer("How many times to report? (max 3000 per account):")

    @dp.message_handler(lambda message: user_report_state.get(message.from_user.id, {}).get('state') == 'awaiting_count')
    async def get_category(message: types.Message):
        try:
            count = int(message.text.strip())
            user_report_state[message.from_user.id]['count'] = min(count, 3000)
        except:
            await message.answer("Please send a number.")
            return
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("Nudity", callback_data="cat_nudity")],
            [InlineKeyboardButton("Pornography", callback_data="cat_porn")],
            [InlineKeyboardButton("Scam", callback_data="cat_scam")],
        ])
        user_report_state[message.from_user.id]['state'] = 'awaiting_category'
        await message.answer("Select report category:", reply_markup=kb)

    @dp.callback_query_handler(lambda c: c.data.startswith("cat_"))
    async def ask_email(callback_query: types.CallbackQuery):
        category = callback_query.data.split("_")[1]
        user_report_state[callback_query.from_user.id]['category'] = category
        user_report_state[callback_query.from_user.id]['state'] = 'awaiting_email'
        await callback_query.message.answer("Enter the email address to send the report to:")

    @dp.message_handler(lambda message: user_report_state.get(message.from_user.id, {}).get('state') == 'awaiting_email')
    async def start_reporting(message: types.Message):
        user_id = message.from_user.id
        email = message.text.strip()
        state = user_report_state[user_id]
        state['email'] = email

        # Load template and replace tags
        format_str = open(FORMAT_FILE).read()
        username = state['username']
        report_msg = format_str.format(
            user_id=user_id,
            username=username,
            name=username.strip('@'),
            date=str(datetime.datetime.now().date())
        )

        await message.answer(
            f"🛠 Starting engines! Will try my best sir.\n"
            f"Category: {state['category']}\n"
            f"Reporting {state['count']} times..."
        )

        # Placeholder for real SMTP + Telethon spam logic
        await message.answer(f"📤 Report content:\n\n{report_msg}")
        user_report_state.pop(user_id, None)
