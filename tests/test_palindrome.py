import pytest
from itertools import chain, product
from palindrome import generate_palindromes
from words import pu_words

small_word_list = ['a', 'ala', 'alasa', 'kala', 'la', 'pu']


def is_palindrome(words: tuple[str, ...]) -> bool:
    caseless_joined = ''.join(words).casefold()
    return caseless_joined == caseless_joined[::-1]


def generate_palindromes_naïvely(word_list: list[str], max_word_count: int) -> list[str]:
    word_combinations = chain.from_iterable(product(word_list, repeat=i) for i in range(1, max_word_count + 1))
    return [' '.join(words) for words in word_combinations if is_palindrome(words)]


@pytest.mark.parametrize('word_list, max_word_count', [
    (pu_words, 3),
    (small_word_list, 8),
])
def test_generate_palindromes(word_list: list[str], max_word_count: int):
    expected = generate_palindromes_naïvely(word_list, max_word_count)
    actual = generate_palindromes(word_list, max_word_count)
    assert sorted(actual) == sorted(expected)


def test_case_insensitiveness():
    cased_word_list = ['ala', 'Ala', 'kALa']
    expected = ['ala', 'Ala', 'ala ala', 'ala Ala', 'Ala ala', 'Ala Ala', 'ala kALa', 'Ala kALa']
    actual = generate_palindromes(cased_word_list, 2)
    assert sorted(actual) == sorted(expected)
