import operator

from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Multiselect, Button, Column, Next, SwitchTo
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory
from aiogram_dialog.widgets.text import Const, Jinja, Format
from aiogram_dialog import Dialog, Window

from bot.dialog.callbacks import get_selected_filters, get_inp_data
from bot.dialog.getters import get_data
from bot.dialog.states import States


class Windows:
    @staticmethod
    def get_start_window():
        return Window(
            Const(
                "<b>Добро пожаловать в рекомендательную систему отзывов! 🎉</b>\n\n"
                "Вы можете настроить фильтры для получения наиболее релевантных отзывов.\n"
                "Пожалуйста, выберите параметры:\n\n"
                "1. 📅 <b>Дата начала и дата конца</b>:\n"
                "   - Укажите диапазон дат в формате <code>YYYY.MM.DD-YYYY.MM.DD</code>, "
                "за который хотите получить отзывы.\n"
                "   - Пример: <code>2023.01.01-2023.12.31</code>\n\n"
                "2. ⚠️ <b>Учитывать неадекватные отзывы</b>:\n"
                "   - Выберите, хотите ли вы учесть неадекватные отзывы.\n\n"
                "3. 🔠 <b>Фильтрация по длине отзыва</b>:\n"
                "   - Укажите минимальную и максимальную длину текста отзыва.\n"
                "   - Пример: <code>50-500</code>\n\n"
                "4. 🔢 <b>Максимальное количество отзывов</b>:\n"
                "   - Укажите, сколько отзывов вы хотите проанализировать.\n"
                "   - Пример: <code>10000</code>\n\n"
                "5. 📝 <b>Фильтрация по ключевым словам</b>:\n"
                "   - Укажите ключевые слова, по которым нужно искать отзывы.\n"
                "   - Пример: <code>коллектив</code>, <code>зарплата</code>\n\n"
                "Приоритет следующий: 1 -> 2 -> 3 -> 4 -> 5"
            ),
            Column(
                Multiselect(
                    Format("✓ {item[0]}"),  # E.g `✓ Apple`
                    Format("{item[0]}"),
                    id="filters",
                    item_id_getter=operator.itemgetter(1),
                    items="data",
                ),
            ),
            Button(Const('Подтвердить ✅'), id='conf', on_click=get_selected_filters),
            getter=get_data,
            state=States.START,
            parse_mode="HTML"
        )

    @staticmethod
    def get_date_filter_window():
        return Window(
            Const(
                "📅 <b>Дата начала и дата конца</b>:\n"
                "   - Укажите диапазон дат в формате <code>YYYY.MM.DD-YYYY.MM.DD</code>, "
                "за который хотите получить отзывы.\n"
                "   - Пример: <code>2023.01.01-2023.12.31</code>\n\n"
            ),
            TextInput(id="date_inp", on_success=get_inp_data('date')),
            state=States.DATE_FILTER,
            parse_mode="HTML"
        )

    @staticmethod
    def get_len_filter_window():
        return Window(
            Const(
                "🔠 <b>Фильтрация по длине отзыва</b>:\n"
                "   - Укажите минимальную и максимальную длину текста отзыва.\n"
                "   - Пример: <code>50-500</code>"
            ),
            TextInput(id="len_inp", on_success=get_inp_data('len')),
            state=States.LEN_FILTER,
            parse_mode="HTML"
        )

    @staticmethod
    def get_count_filter_window():
        return Window(
            Const(
                "🔢 <b>Максимальное количество отзывов</b>:\n"
                "   - Укажите, сколько отзывов вы хотите проанализировать.\n"
                "   - Пример: <code>10000</code>"
            ),
            TextInput(id="cnt_inp", on_success=get_inp_data('count')),
            state=States.COUNT_FILTER,
            parse_mode="HTML"
        )

    @staticmethod
    def get_key_words_filter_window():
        return Window(
            Const(
                "📝 <b>Фильтрация по ключевым словам</b>:\n"
                "   - Укажите ключевые слова, по которым нужно искать отзывы.\n"
                "   - Пример: <code>коллектив</code>, <code>зарплата</code>"
            ),
            TextInput(id="kw_inp", on_success=get_inp_data('key_words')),
            state=States.KEY_WORDS_FILTER,
            parse_mode="HTML"
        )
