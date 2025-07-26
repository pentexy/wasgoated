from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import executor
from config import API_TOKEN

# Initialize
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

# ✅ Basic /start command
@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.answer("✅ Bot is running!")

# ✅ Start the bot
if __name__ == '__main__':
    print("🤖 Bot is running...")
    executor.start_polling(dp, skip_updates=True)
