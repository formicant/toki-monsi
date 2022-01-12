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
|     1 |        5 |       0.001 |       0.023 |
|     2 |       32 |       0.009 |       0.023 |
|     3 |      171 |       0.023 |       0.026 |
|     4 |      840 |       0.125 |       0.041 |
|     5 |     4042 |       0.649 |       0.110 |
|     6 |    19544 |       3.306 |       0.450 |
|     7 |    93782 |      15.674 |       2.097 |
|     8 |   449797 |      76.090 |      10.198 |
|     9 |  2154033 |     364.602 |      51.169 |
|    10 | 10310145 |    1793.520 |     238.331 |
