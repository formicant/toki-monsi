# Toki Pona palindrome generator

## TO DO:

- Test
- Try optimizing
- Try multiprocessing
- Add grammar parser to filter out trash


## Performance

Single-threaded, no grammar parsing:

|words ⩽|    count |  time, s |
|------:|---------:|---------:|
|     1 |        5 |    0.001 |
|     2 |       32 |    0.009 |
|     3 |      171 |    0.023 |
|     4 |      840 |    0.131 |
|     5 |     4042 |    0.677 |
|     6 |    19544 |    3.522 |
|     7 |    93782 |   17.308 |
|     8 |   449797 |   84.703 |
|     9 |  2154033 |  415.266 |
|    10 | 10310145 | 2025.372 |
