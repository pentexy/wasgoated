from aiogram import types
from storage.utils import load_json, save_json
import smtplib

SMTP_FILE = 'data/smtp_accounts.json'
user_smtp_states = {}

def register_add_smtp(dp):
    @dp.callback_query_handler(lambda c: c.data == 'add_smtp')
    async def prompt_email(callback_query: types.CallbackQuery):
        await callback_query.message.answer("Enter SMTP email address:")
        user_smtp_states[callback_query.from_user.id] = {'state': 'awaiting_email'}

    @dp.message_handler(lambda message: user_smtp_states.get(message.from_user.id, {}).get('state') == 'awaiting_email')
    async def handle_email(message: types.Message):
        user_smtp_states[message.from_user.id] = {'state': 'awaiting_password', 'email': message.text.strip()}
        await message.answer("Enter SMTP password:")

    @dp.message_handler(lambda message: user_smtp_states.get(message.from_user.id, {}).get('state') == 'awaiting_password')
    async def handle_password(message: types.Message):
        state = user_smtp_states[message.from_user.id]
        email = state['email']
        password = message.text.strip()
        try:
            smtp = smtplib.SMTP("smtp.gmail.com", 587)
            smtp.starttls()
            smtp.login(email, password)
            smtp.quit()
            smtps = load_json(SMTP_FILE)
            smtps.append({'email': email, 'password': password})
            save_json(SMTP_FILE, smtps)
            await message.answer(f"✅ SMTP Added Successfully!\nEmail: {email}")
        except Exception as e:
            await message.answer(f"Login failed: {e}")
        user_smtp_states.pop(message.from_user.id, None)
