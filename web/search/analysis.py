import re
import string

from Stemmer import Stemmer  # type: ignore

STOPWORDS = {
    "the",
    "be",
    "to",
    "of",
    "and",
    "a",
    "in",
    "that",
    "have",
    "i",
    "it",
    "for",
    "not",
    "on",
    "with",
    "he",
    "as",
    "you",
    "do",
    "at",
    "this",
    "but",
    "his",
    "by",
    "from",
    "ludic",
}

PUNCTUATION = re.compile(f"[{re.escape(string.punctuation)}]")
STEMMER = Stemmer("english")


def tokenize(text: str) -> list[str]:
    return text.split()


def lowercase_filter(tokens: list[str]) -> list[str]:
    return [token.lower() for token in tokens]


def punctuation_filter(tokens: list[str]) -> list[str]:
    return [PUNCTUATION.sub("", token) for token in tokens]


def stopword_filter(tokens: list[str]) -> list[str]:
    return [token for token in tokens if token not in STOPWORDS]


def stem_filter(tokens: list[str]) -> list[str]:
    return STEMMER.stemWords(tokens)  # type: ignore


def analyze(text: str) -> list[str]:
    tokens = tokenize(text)
    tokens = lowercase_filter(tokens)
    tokens = punctuation_filter(tokens)
    tokens = stopword_filter(tokens)
    tokens = stem_filter(tokens)

    return [token for token in tokens if token]
