import argparse
from words import pu_words
from palindrome import PalindromeGenerator
from timeit import default_timer as timer

def generate_palindromes(max_word_count: int):
    print(f'Generating palindromes with <= {max_word_count} words...')
    
    start = timer()
    generator = PalindromeGenerator(pu_words)
    inter = timer()
    palindromes = generator.generate(max_word_count)
    end = timer()
    
    # print()
    # for p in palindromes:
    #     print(p)
    
    print()
    print(f'count: {len(palindromes)}')
    print(f'graph time: {inter - start:.3f} s')
    print(f'total time: {end - start:.3f} s')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate palindromes.')
    parser.add_argument('max_word_count', type=int, help='max word count')
    max_word_count = parser.parse_args().max_word_count
    
    generate_palindromes(max_word_count)
