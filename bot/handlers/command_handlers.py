from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from bot.dialog.states import States


async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(States.START, mode=StartMode.RESET_STACK)
