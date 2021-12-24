from __future__ import annotations
from typing import Iterable
from functools import lru_cache


def reverse(s: str) -> str:
    return s[::-1]


def matches_with_reverse(phrase: str, offset: int=0) -> bool:
    if offset < 0:
        matching_part = phrase[:offset]
    else:
        matching_part = phrase[offset:]
    return matching_part == reverse(matching_part)


class PalindromeFragment:
    """ A palindrome fragment is a sequence of `words`
        partially matching with its reverse.
        The reverse should be padded by a positive or negative `offset`
        in order to match with the original phrase.
    """
    def __init__(self, words: list[str], offset: int):
        self.words = words
        self.offset = offset
        self.words_combined = ''.join(words)
        # assert matches_with_reverse(self.words_combined, self.offset), 'Not a fragment of a palindrome!'
    
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
    
    @lru_cache
    def get_words_by_ending(ending: str) -> list[str]:
        return [word for word in word_list if word.endswith(ending) or ending.endswith(word)]
    
    @lru_cache
    def get_words_by_beginning(beginning: str) -> list[str]:
        return [word for word in word_list if word.startswith(beginning) or beginning.startswith(word)]
    
    def get_possible_prependings(fragment: PalindromeFragment) -> Iterable[PalindromeFragment]:
        """ Tries adding every word from the `word_list` to the beginning of the fragment.
            Returns only valid palindrome fragments.
        """
        matching_part = reverse(fragment.words_combined[fragment.offset:])
        for word in get_words_by_ending(matching_part):
            yield fragment.prepend(word)
    
    def get_possible_appendings(fragment: PalindromeFragment) -> Iterable[PalindromeFragment]:
        """ Tries adding every word from the `word_list` to the end of the fragment.
            Returns only valid palindrome fragments.
        """
        matching_part = reverse(fragment.words_combined[:fragment.offset])
        for word in get_words_by_beginning(matching_part):
            yield fragment.append(word)
    
    def get_possible_extensions_recursively(fragment: PalindromeFragment) -> Iterable[PalindromeFragment]:
        """ Tries adding every possible combinations of words
            to the beginning and the end of the fragment.
            Returns only valid palindrome fragments with <= `max_word_count` words.
        """
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
                if matches_with_reverse(word, offset):
                    yield PalindromeFragment([word], offset)
    
    cores = get_palindrome_cores()
    palindromes = (fragment
        for core in cores
        for fragment in get_possible_extensions_recursively(core)
        if fragment.is_complete()
    )
    return [palindrome.get_phrase() for palindrome in palindromes]
