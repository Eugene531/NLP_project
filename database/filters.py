import pandas as pd
from typing import List


class DataFilters:
    def __init__(self, df: pd.DataFrame):
        self.df: pd.DataFrame = df

    def filter_by_date_range(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Фильтрация по диапазону дат
        """
        mask = (self.df['date'] >= start_date) & (self.df['date'] <= end_date)
        return self.df[mask]


    def filter_by_inadequate_reviews(self, include_inadequate: bool = True) -> pd.DataFrame:
        """
        Фильтрация с учетом/без учета неадекватных отзывов
        (Здесь предполагается, что вы заранее пометили неадекватные отзывы,
        добавив столбец 'adequate' в DataFrame)
        """
        if include_inadequate:
            return self.df
        else:
            return self.df[self.df['adequate'] == True]

    def filter_by_review_length(self, min_length: int, max_length: int) -> pd.DataFrame:
        """
        Фильтрация по длине отзыва
        """
        mask = self.df['text'].apply(lambda x: min_length <= len(x) <= max_length)
        return self.df[mask]

    def filter_by_review_count(self, count: int) -> pd.DataFrame:
        """
        Фильтрация по количеству отзывов
        """
        return self.df.head(count)

    def filter_by_keywords(self, keywords: List[str]) -> pd.DataFrame:
        """
        Фильтрация по ключевым словам
        """
        mask = self.df['text'].apply(lambda x: any(keyword in x for keyword in keywords))
        return self.df[mask]
