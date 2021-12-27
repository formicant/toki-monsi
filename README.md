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

Single-threaded, no grammar parsing:

|words ⩽|    count |  time, s |
|------:|---------:|---------:|
|     1 |        5 |    0.001 |
|     2 |       32 |    0.009 |
|     3 |      171 |    0.023 |
|     4 |      840 |    0.125 |
|     5 |     4042 |    0.649 |
|     6 |    19544 |    3.306 |
|     7 |    93782 |   15.674 |
|     8 |   449797 |   76.090 |
|     9 |  2154033 |  364.602 |
|    10 | 10310145 | 1793.520 |
