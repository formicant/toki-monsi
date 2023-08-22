# Toki Pona palindrome generator

Generates palindromes in Toki Pona.


## Requirements:

- python 3.10
- parsita 2.1
- nltk 3.5
- pytest


## Usage

``` bash
python __main__.py [-h] [-w WORDS] [-g] [-s SORT] [-o OUTPUT] max_word_count
```

positional arguments:
* `max_word_count` - maximum word count

options:
* `-h`, `--help` — show the help message and exit
* `-w WORDS`, `--words WORDS` — which word list to use:
  - `pu` _(default)_ — use only _pu_ words
  - `ku-suli` — use _pu_ and _ku suli_ words
  - `ku-lili` — use _pu_, _ku suli_, and _ku lili_ words
* `-g`, `--grammar` — generate only grammatically valid sentences
* `-s SORT`, -`-sort SORT` — sort results:
  - `A` — alphabetically
  - `L` — by length
  - `W` — by word count
  - `LM` — using an N-gram language model
* `-o OUTPUT`, `--output OUTPUT` — output file (stdout if not specified)


## TO DO:

- Make the grammar work on substrings to filter out whole subtrees when generating palindromes
