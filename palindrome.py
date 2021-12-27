from __future__ import annotations
from typing import Iterable, Optional
from functools import lru_cache


def reverse(s: str) -> str:
    return s[::-1]


class PalindromeFragment:
    """ A palindrome fragment is a sequence of `words`
        partially matching with its reverse.
        The reverse should be padded by a positive or negative `offset`
        in order to match with the original phrase.
    """
    def __init__(self, words: list[str], offset: int):
        self.words = words
        self.offset = offset
    
    @classmethod
    def try_from_single_word(cls, word: str, offset: int) -> Optional[PalindromeFragment]:
        """ Returns a fragment consisting of a single `word` with a given `offset`
            if it is a valid palindrome fragment, or `None` if not.
        """
        if offset < 0:
            matching_part = word[:offset].casefold()
        else:
            matching_part = word[offset:].casefold()
        
        if matching_part == reverse(matching_part):
            return cls([word], offset)
        else:
            return None
    
    def is_complete(self) -> bool:
        """ Is the fragment a complete palindrome?
        """
        return self.offset == 0
    
    def prepend(self, word: str) -> PalindromeFragment:
        """ Returns a new fragment with a new `word` at the beginning
            and all the words from the current fragment.
        """
        return PalindromeFragment([word, *self.words], self.offset + len(word))
    
    def append(self, word: str) -> PalindromeFragment:
        """ Returns a new fragment with all the words
            from the current fragment and a new `word` at the end.
        """
        return PalindromeFragment([*self.words, word], self.offset - len(word))
    
    def get_phrase(self) -> str:
        """ Returns the words separated by spaces.
        """
        return ' '.join(self.words)


def generate_palindromes(word_list: list[str], max_word_count: int) -> list[str]:
    """ Returns a list of all possible palindromes
        with <= `max_word_count` words from `word_list`.
    """
    cased_and_caseless_words = [(word, word.casefold()) for word in word_list]
    
    @lru_cache
    def get_words_by_ending(ending: str) -> list[str]:
        return [word
            for word, caseless_word in cased_and_caseless_words
            if caseless_word.endswith(ending) or ending.endswith(caseless_word)
        ]
    
    @lru_cache
    def get_words_by_beginning(beginning: str) -> list[str]:
        return [word
            for word, caseless_word in cased_and_caseless_words
            if caseless_word.startswith(beginning) or beginning.startswith(caseless_word)
        ]
    
    def get_possible_prependings(fragment: PalindromeFragment) -> Iterable[PalindromeFragment]:
        """ Returns all possible palindrome fragments that differ from
            the given `fragment` by one word added to the beginning.
        """
        matching_part = reverse(fragment.words[-1][fragment.offset:])
        for word in get_words_by_ending(matching_part.casefold()):
            yield fragment.prepend(word)
    
    def get_possible_appendings(fragment: PalindromeFragment) -> Iterable[PalindromeFragment]:
        """ Returns all possible palindrome fragments that differ from
            the given `fragment` by one word added to the end.
        """
        matching_part = reverse(fragment.words[0][:fragment.offset])
        for word in get_words_by_beginning(matching_part.casefold()):
            yield fragment.append(word)
    
    def get_possible_extensions_recursively(fragment: PalindromeFragment) -> Iterable[PalindromeFragment]:
        """ Tries adding every possible combinations of words
            to the beginning and the end of the fragment.
            Returns only valid palindromes with <= `max_word_count` words.
        """
        if fragment.is_complete():
            yield fragment
        
        if len(fragment.words) < max_word_count:
            if fragment.offset < 0:
                possible_extensions = get_possible_prependings(fragment)
            else:
                possible_extensions = get_possible_appendings(fragment)
            
            for extension in possible_extensions:
                yield from get_possible_extensions_recursively(extension)
    
    def get_palindrome_cores() -> Iterable[PalindromeFragment]:
        """ Returns all palindrome fragments consisting of a single word.
        """
        for word in word_list:
            for offset in range(-len(word), len(word)):                   #  .....nanpa
                # `-len(word)` gives a non-intersecting fragment like this:  apnan.....
                # Greater offsets give intersecting fragments like these:
                #     ....nanpa      ..nanpa      nanpa....
                #     apnan....      apnan..      ....apnan
                fragment = PalindromeFragment.try_from_single_word(word, offset)
                if fragment:
                    yield fragment
    
    cores = get_palindrome_cores()
    palindromes = (fragment
        for core in cores
        for fragment in get_possible_extensions_recursively(core)
    )
    return [palindrome.get_phrase() for palindrome in palindromes]
