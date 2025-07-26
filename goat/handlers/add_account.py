from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError

import os
import asyncio
from config import API_ID, API_HASH
from storage.utils import save_json, load_json

ACCOUNTS_FILE = 'data/telegram_accounts.json'

account_login_sessions = {}

class AddAccountStates(StatesGroup):
    waiting_for_phone = State()
    waiting_for_code = State()
    waiting_for_password = State()

def register_add_account(dp):
    @dp.callback_query_handler(lambda c: c.data == 'add_account')
    async def ask_phone(callback_query: types.CallbackQuery, state: FSMContext):
        await callback_query.message.answer("📱 Enter the phone number (with +countrycode):")
        await AddAccountStates.waiting_for_phone.set()

    @dp.message_handler(state=AddAccountStates.waiting_for_phone)
    async def send_code(message: types.Message, state: FSMContext):
        phone = message.text.strip()
        session_name = f"sessions/{phone.replace('+', '')}"
        os.makedirs("sessions", exist_ok=True)
        client = TelegramClient(session_name, API_ID, API_HASH)

        try:
            await client.connect()
            sent = await client.send_code_request(phone)
            account_login_sessions[message.from_user.id] = {
                'client': client,
                'phone': phone,
                'phone_code_hash': sent.phone_code_hash
            }
            await message.answer("✅ Code sent! Now enter the code you received:")
            await AddAccountStates.waiting_for_code.set()
        except Exception as e:
            await message.answer(f"❌ Failed to send code:\n{e}")
            await state.finish()

    @dp.message_handler(state=AddAccountStates.waiting_for_code)
    async def enter_code(message: types.Message, state: FSMContext):
        data = account_login_sessions.get(message.from_user.id)
        if not data:
            await message.answer("Session expired. Please try again.")
            await state.finish()
            return

        code = message.text.strip()
        client = data['client']
        phone = data['phone']
        phone_code_hash = data['phone_code_hash']

        try:
            await client.sign_in(phone=phone, code=code, phone_code_hash=phone_code_hash)
            me = await client.get_me()
            acc_data = {
                "phone": phone,
                "user_id": me.id,
                "name": f"{me.first_name} {me.last_name or ''}".strip(),
                "username": me.username or '',
                "session": session_name
            }

            accounts = load_json(ACCOUNTS_FILE)
            accounts.append(acc_data)
            save_json(ACCOUNTS_FILE, accounts)

            await message.answer(
                f"✅ Account Added Successfully!\n📞 Number: {phone}\n🧾 Total Added Accs: {len(accounts)}",
                reply_markup=ReplyKeyboardRemove()
            )
            await client.disconnect()
            account_login_sessions.pop(message.from_user.id, None)
            await state.finish()

        except SessionPasswordNeededError:
            await message.answer("🔐 This account has 2FA enabled. Enter the password:")
            await AddAccountStates.waiting_for_password.set()
        except PhoneCodeInvalidError:
            await message.answer("❌ Invalid code. Try again:")
        except Exception as e:
            await message.answer(f"❌ Error: {e}")
            await client.disconnect()
            await state.finish()

    @dp.message_handler(state=AddAccountStates.waiting_for_password)
    async def enter_2fa_password(message: types.Message, state: FSMContext):
        data = account_login_sessions.get(message.from_user.id)
        if not data:
            await message.answer("Session expired. Please try again.")
            await state.finish()
            return

        password = message.text.strip()
        client = data['client']

        try:
            await client.sign_in(password=password)
            me = await client.get_me()
            acc_data = {
                "phone": data['phone'],
                "user_id": me.id,
                "name": f"{me.first_name} {me.last_name or ''}".strip(),
                "username": me.username or '',
                "session": data['client'].session.filename
            }

            accounts = load_json(ACCOUNTS_FILE)
            accounts.append(acc_data)
            save_json(ACCOUNTS_FILE, accounts)

            await message.answer(
                f"✅ 2FA Login Successful!\n📞 Number: {data['phone']}\n🧾 Total Added Accs: {len(accounts)}"
            )
            await client.disconnect()
            account_login_sessions.pop(message.from_user.id, None)
            await state.finish()
        except Exception as e:
            await message.answer(f"❌ 2FA Error: {e}")
            await client.disconnect()
            await state.finish()
