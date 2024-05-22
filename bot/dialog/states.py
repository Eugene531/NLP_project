from aiogram.filters.state import StatesGroup, State


class States(StatesGroup):
    START = State()
    DATE_FILTER = State()
    LEN_FILTER = State()
    COUNT_FILTER = State()
    KEY_WORDS_FILTER = State()
    GET_RECOMMENDATIONS = State()
    GET_FEED_BACK = State()
    GET_STATS = State()
