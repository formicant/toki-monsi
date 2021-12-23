from words import pu_words
from palindrome import generate_palindromes
from timeit import default_timer as timer

if __name__ == '__main__':
    
    max_word_count = 6
    print(f'Generating palindromes with <= {max_word_count} words...')
    
    start = timer()
    palindromes = generate_palindromes(pu_words, max_word_count)
    end = timer()
    
    print()
    for p in palindromes:
        print(p)
    
    print()
    print(f'count: {len(palindromes)}')
    print(f'elapsed: {end - start:.3f} s')
