import pandas as pd
import numpy as np
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
import random
from tqdm.auto import tqdm, trange
import os
from sklearn.model_selection import train_test_split


df = pd.read_csv('/content/train.csv', sep=',')
df_train, df_test = train_test_split(df.dropna(), test_size=0.5, random_state=1)
pairs = df_train[['X', 'Y']].values.tolist()

raw_model = '0x7194633/keyt5-large'
model = T5ForConditionalGeneration.from_pretrained(raw_model).cuda()
tokenizer = T5Tokenizer.from_pretrained(raw_model)

optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)

batch_size = 4  # сколько примеров показывем модели за один шаг
report_steps = 200  # раз в сколько шагов печатаем результат
epochs = 3  # сколько раз мы покажем данные модели

model.train()
losses = []
for epoch in range(epochs):
    print('EPOCH', epoch)
    random.shuffle(pairs)
    for i in trange(0, int(len(pairs) / batch_size)):
        batch = pairs[i * batch_size: (i + 1) * batch_size]
        x = tokenizer([p[0] for p in batch], return_tensors='pt', padding=True).to(model.device)
        y = tokenizer([p[1] for p in batch], return_tensors='pt', padding=True).to(model.device)
        y.input_ids[y.input_ids == 0] = -100
        loss = model(
            input_ids=x.input_ids,
            attention_mask=x.attention_mask,
            labels=y.input_ids,
            decoder_attention_mask=y.attention_mask,
            return_dict=True
        ).loss
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        losses.append(loss.item())
        if i % report_steps == 0:
            print('step', i, 'loss', np.mean(losses[-report_steps:]))

model.eval()


def answer(x, **kwargs):
    inputs = tokenizer(x, return_tensors='pt').to(model.device)
    with torch.no_grad():
        hypotheses = model.generate(**inputs, **kwargs)
    return tokenizer.decode(hypotheses[0], skip_special_tokens=True)
