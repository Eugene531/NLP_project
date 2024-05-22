import os
import torch
from transformers import BertTokenizer, BertForSequenceClassification


# Путь, где сохранена модель и токенизатор
model_save_path = os.path.join(os.getcwd(), "configs", "classif")

# Загрузка модели и токенизатора
model = BertForSequenceClassification.from_pretrained(model_save_path)
tokenizer = BertTokenizer.from_pretrained(model_save_path)


# Функция для классификации
def predict(text):
    # Токенизация текста
    inputs = tokenizer(text, padding=True, truncation=True, max_length=64, return_tensors="pt")

    # Передача токенизированных данных в модель
    with torch.no_grad():
        outputs = model(**inputs)

    # Получение вероятностей и выбор наиболее вероятного класса
    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    predicted_class = torch.argmax(predictions).item()  # 0 - norm, 1 - bad
    return predicted_class, predictions[0][predicted_class].item()
