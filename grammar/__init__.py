from .toki_pona_grammar import TokiPonaGrammar
import multiprocessing

MIN_SENTENCE_COUNT_FOR_MULTIPROCESSING = 500

def grammar_filter(sentences: list[str], word_list: list[str]) -> list[str]:
    if len(sentences) < MIN_SENTENCE_COUNT_FOR_MULTIPROCESSING:
        # single process
        return filter_chunk((sentences, word_list))
    else:
        # multiprocessing
        chunk_count = multiprocessing.cpu_count()
        chunks = ((sentences[i::chunk_count], word_list) for i in range(chunk_count))
        pool = multiprocessing.Pool()
        results = pool.imap(filter_chunk, chunks)
        return [s for list in results for s in list]


def filter_chunk(context: tuple[list[str], list[str]]) -> list[str]:
    sentences, word_list = context
    grammar = TokiPonaGrammar(word_list)
    return [s for s in sentences if grammar.is_valid(s)]