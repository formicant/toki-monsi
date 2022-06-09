import pytest

from corpus import get_valid_sentences, get_invalid_sentences
from grammar import is_valid


@pytest.mark.parametrize('sentence', get_valid_sentences())
def test_valid_sentences(sentence: str):
    assert is_valid(sentence)


@pytest.mark.parametrize('sentence', get_invalid_sentences())
def test_invalid_sentence(sentence: str):
    assert not is_valid(sentence)
