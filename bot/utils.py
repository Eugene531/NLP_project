from aiogram.types import Message

from classifier.model import predict
from database.filters import DataFilters
from summarizer.model import get_recs


async def send_recs_to_user(message: Message, dialog_data):
    data_filter: DataFilters = dialog_data['data_filter']

    # Фильтр по дате
    if date := dialog_data.get('date'):
        start, end = date.split('-')
        data_filter.df = data_filter.filter_by_date_range(start, end)
    # НЕ учитывать неадекватные
    if not dialog_data.get('inadequate'):
        valid_texts = use_classifier(data_filter.df)
        data_filter.df = data_filter.df[data_filter.df['text'].isin(valid_texts)]
    # Фильтр по длине текста
    if text_len := dialog_data.get('len'):
        len_min, len_max = text_len.split('-')
        data_filter.df = data_filter.filter_by_review_length(int(len_min), int(len_max))
    # Фильтр по кол-ву отзывов
    if count := dialog_data.get('count'):
        data_filter.df = data_filter.filter_by_review_count(int(count))
    # Фильтр по ключевым словам
    if key_words := dialog_data.get('key_words'):
        data_filter.df = data_filter.filter_by_keywords(key_words.split(','))

    text = data_filter.df['text']

    must_have, maybe = get_recs(text)
    data_to_send = (
            "Вам обязательно нужно учесть:\n"
            + "\n".join([f"- {item}" for item in must_have]) + "\n\n"
            "Обратите внимание на:\n"
            + "\n".join([f"- {item}" for item in maybe])
    )

    chat_id = message.chat.id
    await message.bot.send_message(chat_id, data_to_send)


def use_classifier(df) -> list[str]:
    texts = df['text']

    valid_texts = []
    for text in texts:
        predicted_class, predicted_probability = predict(text)
        if predicted_class == 0:
            valid_texts.append(text)
    return valid_texts
