import multiprocessing
from parsita import Success
from .parser import TokiPonaParser

MIN_SENTENCE_COUNT_FOR_MULTIPROCESSING = 500


def grammar_filter(sentences: list[str]) -> list[str]:
    if len(sentences) < MIN_SENTENCE_COUNT_FOR_MULTIPROCESSING:
        # single process
        return filter_chunk(sentences)
    else:
        # multiprocessing
        chunk_count = multiprocessing.cpu_count()
        chunks = (sentences[i::chunk_count] for i in range(chunk_count))
        pool = multiprocessing.Pool()
        results = pool.imap(filter_chunk, chunks)
        return [s for list in results for s in list]


def filter_chunk(sentences: list[str]) -> list[str]:
    return [s for s in sentences if is_valid(s)]


def is_valid(sentence: str) -> bool:
    result = TokiPonaParser.sentence.parse(sentence)
    return isinstance(result, Success)
