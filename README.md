# Toki Pona palindrome generator

## Requirements:

- python 3.10
- parsita
- pytest

## TO DO:

- Add sorting
- Add grammar parser to filter out trash
- Rate results (according to n-gram frequencies or something else)


## Performance

Old algorithm (direct generating) vs new algorithm (using a graph):

|words ⩽|    count |time (old), s|time (mid), s|time (new), s|
|------:|---------:|------------:|------------:|------------:|
|     1 |        5 |       0.001 |       0.022 |       0.044 |
|     2 |       32 |       0.009 |       0.023 |       0.045 |
|     3 |      171 |       0.023 |       0.026 |       0.047 |
|     4 |      840 |       0.125 |       0.039 |       0.054 |
|     5 |     4042 |       0.649 |       0.101 |       0.090 |
|     6 |    19544 |       3.306 |       0.396 |       0.260 |
|     7 |    93782 |      15.674 |       1.926 |       0.464 |
|     8 |   449797 |      76.090 |       9.059 |       1.301 |
|     9 |  2154033 |     364.602 |      45.591 |       4.723 |
|    10 | 10310145 |    1793.520 |     210.363 |      21.835 |
