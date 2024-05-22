# !pip install transformers sentencepiece
# !pip install torch
# !pip install sentence-transformers
from sentence_transformers import SentenceTransformer
from itertools import groupby
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer


model_name = "0x7194633/keyt5-base"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Инициализация модели для получения эмбеддингов
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')


def generate(text, **kwargs):
    inputs = tokenizer(text, return_tensors='pt')
    with torch.no_grad():
        hypotheses = model.generate(**inputs, num_beams=5, **kwargs)
    s = tokenizer.decode(hypotheses[0], skip_special_tokens=True)
    s = s.replace('; ', ';').replace(' ;', ';').lower().split(';')[:-1]
    s = [el for el, _ in groupby(s)]
    return s


def get_recs(article: list[str]) -> tuple:
    key_words = {}

    for art in article:
        new_key_words = list(generate(art, top_p=1.0, max_length=64))
        for kw in new_key_words:
            key_words[kw] = key_words.get(kw, 0) + 1

    key_words = sorted(key_words, key=lambda n: n[1])

    must_have = key_words[:3]
    maybe = key_words[3:5]
    return must_have, maybe
