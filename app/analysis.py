from typing import Iterable, List, Optional, Set

import pandas as pd
import jieba


def load_stopwords(path: Optional[str]) -> Optional[Set[str]]:
    if not path:
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            words = {line.strip() for line in f if line.strip()}
        return words
    except Exception:
        return None


def tokenize_titles(titles: Iterable[str], stopwords: Optional[Set[str]] = None) -> List[str]:
    words: List[str] = []
    for title in titles:
        if not isinstance(title, str):
            continue
        tokens = jieba.lcut(title)
        for w in tokens:
            w = w.strip()
            if not w:
                continue
            if stopwords and w in stopwords:
                continue
            if len(w) <= 1:
                continue
            words.append(w)
    return words


def frequency_count(words: List[str]) -> pd.Series:
    return pd.Series(words).value_counts()


def analyze_csv(input_csv: str, stopwords_path: Optional[str], top_n: int) -> pd.Series:
    df = pd.read_csv(input_csv)
    titles = df.get("title", [])
    sw = load_stopwords(stopwords_path)
    words = tokenize_titles(titles, stopwords=sw)
    freq = frequency_count(words)
    return freq.head(top_n)


def analyze_items(items: List[dict], stopwords_path: Optional[str], top_n: int) -> pd.Series:
    titles = []
    for it in items:
        if not isinstance(it, dict):
            continue
        title = it.get("title")
        if isinstance(title, str):
            titles.append(title)
    sw = load_stopwords(stopwords_path)
    words = tokenize_titles(titles, stopwords=sw)
    freq = frequency_count(words)
    return freq.head(top_n)