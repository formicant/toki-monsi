from typing import Iterable
from graph import PalindromeGraph, Node

class PalindromeGenerator:
    """ Generates palindromes using words from `word_list`.
    """
    def __init__(self, word_list: Iterable[str]):
        self.graph = PalindromeGraph(word_list)
    
    def generate(self, max_word_count: int) -> list[str]:
        """ Returns a list of all possible palindromes with <= `max_word_count` words.
        """
        palindromes: list[str] = []
        for node, word in self.graph.start_nodes:
            self._get_palindromes_recursively(node, [word], max_word_count, palindromes)
        
        return palindromes
    
    def _get_palindromes_recursively(self, node: Node, words: list[str], max_word_count: int, output: list[str]):
        distance = self.graph.distances[node]
        if distance < max_word_count:
            if distance == 0:
                output.append(' '.join(words))
            
            for edge in self.graph.edges_by_from_node[node]:
                new_words = [*words, edge.word] if node.offset >= 0 else [edge.word, *words]
                self._get_palindromes_recursively(edge.to_node, new_words, max_word_count - 1, output)
