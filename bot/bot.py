from aiogram.filters import CommandStart, Command, ExceptionTypeFilter
from aiogram import Bot, Dispatcher, Router
from aiogram_dialog.api.exceptions import UnknownIntent, NoContextError
from aiogram_dialog import setup_dialogs, Dialog

import bot.handlers.command_handlers as cmd
from bot.dialog.windows import Windows


# Инициализация бота
bot = Bot('')
dp = Dispatcher()
router = Router()

# Инициализация диалога
main_dialog = Dialog(
    Windows.get_start_window(),
    Windows.get_date_filter_window(),
    Windows.get_len_filter_window(),
    Windows.get_count_filter_window(),
    Windows.get_key_words_filter_window(),
)

# Подключение диалога к боту
dp.include_router(main_dialog)
dp.include_router(router)
setup_dialogs(dp)

# Регистрации всех handlers
dp.message.register(cmd.start, CommandStart())
