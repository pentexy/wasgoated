from aiogram import types
from config import OWNER_USERNAME

def register_owner(dp):
    @dp.callback_query_handler(lambda c: c.data == 'owner')
    async def handle_owner(callback_query: types.CallbackQuery):
        await callback_query.message.answer(f"Contact Owner: {OWNER_USERNAME}")
