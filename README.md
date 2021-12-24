# Toki Pona palindrome generator

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
|     3 |      171 |    0.025 |
|     4 |      840 |    0.141 |
|     5 |     4042 |    0.736 |
|     6 |    19544 |    3.769 |
|     7 |    93782 |   18.329 |
|     8 |   449797 |   88.442 |
|     9 |  2154033 |  432.078 |
|    10 | 10310145 | 2107.368 |
