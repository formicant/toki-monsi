from typing import Iterable
from os import listdir
from os.path import isfile, join
import re

def get_valid_sentences():
    return get_corpus('corpus/toki_pona')


def get_invalid_sentences():
    return get_corpus('corpus/toki_ike')


def get_corpus(path: str) -> Iterable[str]:
    for file_path in get_files(path):
        yield from get_sentences(file_path)


def get_files(path: str) -> Iterable[str]:
    entries = (join(path, entry) for entry in listdir(path))
    return (entry for entry in entries if isfile(entry))


def get_sentences(file_path: str) -> Iterable[str]:
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            without_comment = line.split('#', 1)[0]
            for sentence in sentence_end.split(without_comment):
                normalized = non_letter.sub(sentence, ' ').strip()
                if normalized:
                    yield normalized


sentence_end = re.compile(r'[.?!:"“”]')
non_letter = re.compile(r'[^A-Za-z]+')
