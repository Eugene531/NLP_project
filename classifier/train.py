from transformers import BertTokenizer, BertForSequenceClassification
from transformers import Trainer, TrainingArguments
import pandas as pd
import torch
from sklearn.model_selection import train_test_split


# Загрузка модели и токенизатора
model_name = "DeepPavlov/rubert-base-cased-sentence"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

# Загрузка данных
data_normal = pd.read_excel('dataset_normal.xlsx')
data_not_normal = pd.read_excel('dataset_not_normal.xlsx')

data_normal_sampled = data_normal.sample(n=4000, random_state=42)
data_not_normal_sampled = data_not_normal.sample(n=4000, random_state=42)

# Объединение данных
data = pd.concat([data_normal_sampled, data_not_normal_sampled], ignore_index=True)

# Разделение на обучающую и валидационную выборки
train_texts, val_texts, train_labels, val_labels = train_test_split(
    data['text'], data['labels'], test_size=0.2, random_state=42
)

# Токенизация данных
train_encodings = tokenizer(list(train_texts), truncation=True, padding=True, max_length=128)
val_encodings = tokenizer(list(val_texts), truncation=True, padding=True, max_length=128)


class Dataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)


# Создание датасетов
train_dataset = Dataset(train_encodings, list(train_labels))
val_dataset = Dataset(val_encodings, list(val_labels))

training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=1,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    warmup_steps=500,
    weight_decay=0.01,
    learning_rate=2e-5,
    evaluation_strategy='epoch',
    logging_dir='./logs',
    dataloader_num_workers=4
)

# Тренировка модели
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset
)

trainer.train()

# Оценка модели
evaluation_results = trainer.evaluate()
print(evaluation_results)
