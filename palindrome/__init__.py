from dataclasses import dataclass
from typing import Iterable, Tuple
import multiprocessing
from .graph import PalindromeGraph, Node, StartEdge, Edge

MIN_WORD_COUNT_FOR_MULTIPROCESSING = 7

class PalindromeGenerator:
    """ Generates palindromes using words from `word_list`.
    """
    def __init__(self, word_list: list[str]):
        self.graph = PalindromeGraph(word_list)
    
    def generate(self, max_word_count: int) -> list[str]:
        """ Returns a list of all possible palindromes with <= `max_word_count` words.
        """
        # prepare data for processing
        contexts = (
            ProcessContext(start_edge, self.graph.edges_from_node, self.graph.distances, max_word_count)
            for start_edge in self.graph.start_edges
        )
        
        # processing
        results: Iterable[list[str]]
        if max_word_count < MIN_WORD_COUNT_FOR_MULTIPROCESSING:
            # single process
            results = map(get_palindromes_by_start_edge, contexts)
        else:
            # multiprocessing
            pool = multiprocessing.Pool()
            results = pool.imap(get_palindromes_by_start_edge, contexts)
        
        palindromes = [palindrome for list in results for palindrome in list]
        
        return palindromes


@dataclass
class ProcessContext:
    """ Encapsulates data needed to call `get_palindrome_words`.
        Helps avoiding pickling local objects during multiprocessing.
    """
    start_edge: StartEdge
    edges_from_node: dict[Node, list[Edge]]
    distances: dict[Node, int]
    max_word_count: int


def get_palindromes_by_start_edge(context: ProcessContext) -> list[str]:
    """ Gets a list of all palindromes starting with the given start node.
        Can be executed in a separate process.
    """
    palindromes: list[str] = []
    
    # Palindromes are paths in the graph starting with a start edge
    # and ending with the final node.
    # Find all such paths of length <= `max_word_count` from the given `statr_edge`
    stack: list[Tuple[Node, int, str]] = [
        (context.start_edge.to_node, context.max_word_count - 1, context.start_edge.word)
    ]
    while len(stack) > 0:
        (node, words_left, words) = stack.pop()
        distance = context.distances.get(node)
        
        if distance is not None and distance <= words_left:
            if words_left > 0:
                for edge in context.edges_from_node[node]:
                    if node.offset >= 0:
                        new_words = f'{words} {edge.word}'
                    else:
                        new_words = f'{edge.word} {words}'
                    
                    stack.append((edge.to_node, words_left - 1, new_words))
            
            if distance == 0:
                palindromes.append(words)
    
    return palindromes
