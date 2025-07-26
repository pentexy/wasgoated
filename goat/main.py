from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import executor
from goat.config import API_TOKEN

# Import handler registrations
from goat.handlers.start import register_start
from goat.handlers.add_account import register_add_account
from goat.handlers.add_smtp import register_add_smtp
from goat.handlers.report import register_report
from goat.handlers.owner import register_owner

# Setup storage and bot
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

# Register all handlers
register_start(dp)
register_add_account(dp)
register_add_smtp(dp)
register_report(dp)
register_owner(dp)

if __name__ == '__main__':
    print("🤖 Bot is running...")
    executor.start_polling(dp, skip_updates=True)
