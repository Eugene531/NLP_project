from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button

import database.orm as orm
from bot.dialog.states import States
from bot.utils import send_recs_to_user
from database import filters
from database.filters import DataFilters


async def get_selected_filters(
        call_back: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    dialog_data = dialog_manager.dialog_data

    # Получение данных о выбранных кнопках
    widget = dialog_manager.dialog().find('filters')

    selected_filters = sorted(widget.get_checked(dialog_manager))

    all_reviews = orm.get_all_reviews()

    data_filter = DataFilters(all_reviews)

    dialog_data['data_filter']: DataFilters = data_filter
    dialog_data['filters_states']: list = []
    stack_point: int = 1
    dialog_data['stack_point']: int = stack_point

    dialog_data['inadequate'] = False
    if '2' in selected_filters:
        dialog_data['inadequate'] = True

    all_filters = {
        '1': States.DATE_FILTER,
        '3': States.LEN_FILTER,
        '4': States.COUNT_FILTER,
        '5': States.KEY_WORDS_FILTER,
    }

    for filter_id in selected_filters:
        filter_state = all_filters.get(filter_id)
        if filter_state:
            dialog_data['filters_states'] += [filter_state]

    if dialog_data['filters_states']:
        await dialog_manager.switch_to(dialog_data['filters_states'][0])
    else:
        await send_recs_to_user(call_back.message, dialog_data)


def get_inp_data(name):
    async def get_data(
        message: Message,
        managed_text_input: ManagedTextInput[str],
        dialog_manager: DialogManager,
        input_data: str
    ) -> None:
        dialog_data = dialog_manager.dialog_data
        dialog_data[name] = input_data

        if dialog_data['stack_point'] < len(dialog_data['filters_states']):
            next_state = dialog_data['filters_states'][dialog_data['stack_point']]
            dialog_data['stack_point'] += 1
            await dialog_manager.switch_to(next_state)
        else:
            await send_recs_to_user(message, dialog_data)
    return get_data
