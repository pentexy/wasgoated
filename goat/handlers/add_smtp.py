from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

from aiogram import Dispatcher
from goat.storage.utils import save_json, load_json
from goat.states import SMTPStates

SMTP_FILE = 'goat/data/smtp_accounts.json'

def register_add_smtp(dp: Dispatcher):
    @dp.callback_query_handler(lambda c: c.data == 'add_smtp')
    async def start_smtp(callback_query: types.CallbackQuery, state: FSMContext):
        await callback_query.message.answer("Enter SMTP email address:")
        await SMTPStates.waiting_for_email.set()

    @dp.message_handler(state=SMTPStates.waiting_for_email)
    async def get_smtp_email(message: types.Message, state: FSMContext):
        await state.update_data(email=message.text.strip())
        await message.answer("Enter SMTP password:")
        await SMTPStates.waiting_for_password.set()

    @dp.message_handler(state=SMTPStates.waiting_for_password)
    async def get_smtp_password(message: types.Message, state: FSMContext):
        await state.update_data(password=message.text.strip())

        # Provide SES region host choices
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("US East", callback_data="host:email-smtp.us-east-1.amazonaws.com"),
            InlineKeyboardButton("US West", callback_data="host:email-smtp.us-west-2.amazonaws.com"),
            InlineKeyboardButton("EU Central", callback_data="host:email-smtp.eu-central-1.amazonaws.com")
        )
        await message.answer("Choose your SMTP host:", reply_markup=markup)
        await SMTPStates.waiting_for_host.set()

    @dp.callback_query_handler(lambda c: c.data.startswith("host:"), state=SMTPStates.waiting_for_host)
    async def get_smtp_host(callback_query: types.CallbackQuery, state: FSMContext):
        host = callback_query.data.split("host:")[1]
        await state.update_data(host=host)
        await callback_query.message.edit_text(f"SMTP host set to: {host}\nNow enter SMTP port (e.g., 587):")
        await SMTPStates.waiting_for_port.set()

    @dp.message_handler(state=SMTPStates.waiting_for_port)
    async def get_smtp_port(message: types.Message, state: FSMContext):
        try:
            port = int(message.text.strip())
        except ValueError:
            return await message.answer("Invalid port. Please enter a numeric value like 587.")
        
        data = await state.get_data()
        email, password, host = data['email'], data['password'], data['host']

        try:
            smtp = smtplib.SMTP(host, port)
            smtp.starttls()
            smtp.login(email, password)
            smtp.quit()
        except Exception as e:
            await message.answer(f"Login failed: {e}")
            await state.finish()
            return

        # Save SMTP
        smtp_list = load_json(SMTP_FILE)
        smtp_list.append({
            "email": email,
            "password": password,
            "host": host,
            "port": port
        })
        save_json(SMTP_FILE, smtp_list)

        await message.answer(f"✅ SMTP added successfully!\nEmail: {email}\nHost: {host}:{port}", reply_markup=ReplyKeyboardRemove())
        await state.finish()
