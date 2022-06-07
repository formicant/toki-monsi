import pytest
from corpus import get_valid_sentences, get_invalid_sentences
from grammar import TokiPonaGrammar
from words import pu_words

@pytest.mark.parametrize('sentence', get_valid_sentences())
def test_valid_sentences(sentence: str):
    grammar =  TokiPonaGrammar(pu_words)
    assert grammar.is_valid(sentence)


@pytest.mark.parametrize('sentence', get_invalid_sentences())
def test_invalid_sentence(sentence: str):
    grammar =  TokiPonaGrammar(pu_words)
    assert not grammar.is_valid(sentence)
