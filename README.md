# Toki Pona palindrome generator

## Requirements:

- python 3.9 or later
- pytest
- mypy

## TO DO:

- Try optimizing
- Try multiprocessing
- Add grammar parser to filter out trash
- Rate results (according to n-gram frequencies or something else)


## Performance

Old algorithm (direct generating) vs new algorithm (using a graph):

|words ⩽|    count |time (old), s|time (new), s|
|------:|---------:|------------:|------------:|
|     1 |        5 |       0.001 |       0.022 |
|     2 |       32 |       0.009 |       0.023 |
|     3 |      171 |       0.023 |       0.026 |
|     4 |      840 |       0.125 |       0.039 |
|     5 |     4042 |       0.649 |       0.101 |
|     6 |    19544 |       3.306 |       0.396 |
|     7 |    93782 |      15.674 |       1.926 |
|     8 |   449797 |      76.090 |       9.059 |
|     9 |  2154033 |     364.602 |      45.591 |
|    10 | 10310145 |    1793.520 |     210.363 |
