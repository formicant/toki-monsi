import argparse
from typing import Optional, Callable, Any
from timing import Timing
from words import pu_words
from palindrome import PalindromeGenerator
from grammar import TokiPonaGrammar

def generate_palindromes(max_word_count: int, check_grammar: bool, sort_criterion: str, file_name: Optional[str]=None):
    if file_name:
        print(f'Generating palindromes with <= {max_word_count} words...')
    
    word_list = pu_words
    
    timing = Timing()
    
    generator = PalindromeGenerator(word_list)
    timing.mark('graph')
    
    palindromes = generator.generate(max_word_count)
    timing.mark('generation')
    
    if check_grammar:
        grammar = TokiPonaGrammar(word_list)
        palindromes = [p for p in palindromes if grammar.is_valid(p)]
        timing.mark('grammar')
    
    if sort_criterion:
        sort_key = get_sort_key(sort_criterion.lower())
        palindromes.sort(key=sort_key)
        timing.mark('sorting')
    
    if file_name:
        write_to_file(file_name, palindromes)
    else:
        write_to_stdout(palindromes)
    timing.mark('output')
    
    if file_name:
        print(f'Palindrome count: {len(palindromes)}')
        print('Elapsed time:')
        print(timing)


def get_sort_key(value: str) -> Callable[[str], Any]:
    match value:
        case 'a' | 'alphabetical':
            return lambda s: s
        case 'l' | 'length':
            return lambda s: (len(s), s)
        case 'w' | 'word-count':
            return lambda s: (s.count(' '), s)
        case _:
            raise Exception('invalid sorting criterion')


def write_to_stdout(palindromes: list[str]):
    for palindrome in palindromes:
        print(palindrome)


def write_to_file(file_name: str, palindromes: list[str]):
    with open(file_name, 'w', encoding='utf-8') as file:
        for palindrome in palindromes:
            file.write(f'{palindrome}\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generates palindromes in toki pona.')
    parser.add_argument('max_word_count', type=int, help='max word count')
    parser.add_argument('-g', '--grammar', action='store_true', help='check grammar')
    parser.add_argument('-s', '--sort', type=str, help='result sorting: A[lphabetical], L[ength], or W[ord-count]')
    parser.add_argument('-o', '--output', type=str, help='output file (stdout if not specified)')
    
    args = parser.parse_args()
    
    generate_palindromes(args.max_word_count, args.grammar, args.sort, args.output)
