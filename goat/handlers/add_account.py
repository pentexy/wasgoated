from aiogram import types
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from config import API_ID, API_HASH
from storage.utils import load_json, save_json
import os

ACCOUNTS_FILE = 'data/telegram_accounts.json'
SESSIONS_DIR = 'data/sessions'
os.makedirs(SESSIONS_DIR, exist_ok=True)

user_states = {}

def register_add_account(dp):
    @dp.callback_query_handler(lambda c: c.data == 'add_account')
    async def prompt_phone(callback_query: types.CallbackQuery):
        await callback_query.message.answer("Send the phone number to login (with +country_code)")
        user_states[callback_query.from_user.id] = {'state': 'awaiting_phone'}

    @dp.message_handler(lambda message: user_states.get(message.from_user.id, {}).get('state') == 'awaiting_phone')
    async def handle_phone(message: types.Message):
        phone = message.text.strip()
        client = TelegramClient(StringSession(), API_ID, API_HASH)
        await client.connect()
        try:
            await client.send_code_request(phone)
            session_str = client.session.save()
            user_states[message.from_user.id] = {
                'state': 'awaiting_code',
                'phone': phone,
                'session': session_str
            }
            await message.answer("OTP sent. Please enter the code:")
        except Exception as e:
            await message.answer(f"Error: {e}")

    @dp.message_handler(lambda message: user_states.get(message.from_user.id, {}).get('state') == 'awaiting_code')
    async def handle_code(message: types.Message):
        code = message.text.strip()
        state = user_states.get(message.from_user.id, {})
        client = TelegramClient(StringSession(state['session']), API_ID, API_HASH)
        await client.connect()
        try:
            await client.sign_in(phone=state['phone'], code=code)
        except Exception as e:
            if '2FA' in str(e):
                user_states[message.from_user.id]['state'] = 'awaiting_2fa'
                await message.answer("2FA enabled. Please send your password:")
                return
            await message.answer(f"Login failed: {e}")
            return
        await client.disconnect()
        save_account(state['phone'], state['session'])
        await message.answer(f"✅ Account Added Successfully!\nNumber: {state['phone']}")
        user_states.pop(message.from_user.id, None)

    @dp.message_handler(lambda message: user_states.get(message.from_user.id, {}).get('state') == 'awaiting_2fa')
    async def handle_2fa(message: types.Message):
        password = message.text.strip()
        state = user_states.get(message.from_user.id, {})
        client = TelegramClient(StringSession(state['session']), API_ID, API_HASH)
        await client.connect()
        try:
            await client.sign_in(password=password)
            await client.disconnect()
            save_account(state['phone'], state['session'])
            await message.answer(f"✅ Account Added Successfully!\nNumber: {state['phone']}")
        except Exception as e:
            await message.answer(f"2FA login failed: {e}")
        user_states.pop(message.from_user.id, None)

def save_account(phone, session):
    accounts = load_json(ACCOUNTS_FILE)
    accounts.append({'phone': phone, 'session': session})
    save_json(ACCOUNTS_FILE, accounts)
