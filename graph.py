from __future__ import annotations
from typing import Iterable, Optional
from dataclasses import dataclass
from collections import defaultdict
from math import inf
from queue import PriorityQueue
from prioritized import Prioritized

def reverse(s: str) -> str:
    return s[::-1]

def slice_by_offset(word: str, offset: int) -> tuple[str, str]:
    if offset < 0:
        return (word[:offset], word[offset:])
    else:
        return (word[offset:], word[:offset])


@dataclass(frozen=True)
class Node:
    """ Graph node representing a class of palindrome fragments with a common tail.
        Tails are stored with their characters in reversed order.
        `offset` is the signed length of the tail.
        If the tail is located before the pallindromic part, `offset` is >= 0,
        otherwise, `offset` is < 0.
    """
    reversed_tail: str
    offset: int
    
    def __post_init__(self):
        assert(len(self.reversed_tail) == abs(self.offset))


@dataclass(frozen=True)
class Edge:
    """ Edge between two graph nodes marked with a word.
        The edge exists iff `to_node` is reached by adding `word`
        to fragments from `from_node` class.
    """
    from_node: Node
    word: str
    to_node: Node
    
    @classmethod
    def try_create(cls, from_node: Node, word: str) -> Optional[Edge]:
        """ Creates an edge by its `from_node` and `word`
            or returns None if is impossible.
        """
        caseless_word = word.casefold()
        from_tail = from_node.reversed_tail
        from_offset = from_node.offset
        word_offset = (1 if from_offset >= 0 else -1) * len(caseless_word)
        to_offset = from_offset - word_offset
        
        if (from_offset >= 0) == (to_offset >= 0):
            to_tail, tail_matching_part = slice_by_offset(from_tail, word_offset)
            word_matching_part = caseless_word
        else:
            tail, word_matching_part = slice_by_offset(caseless_word, from_offset)
            to_tail = reverse(tail)
            tail_matching_part = from_tail
        
        if tail_matching_part == word_matching_part:
            return Edge(from_node, word, Node(to_tail, to_offset))
        else:
            return None


class PalindromeGraph:
    """ Helper graph to build palindromes.
    """
    
    start_nodes: list[tuple[Node, str]]
    """ Nodes and corresponding words palindrome building can start from. """
    
    edges_by_from_node: dict[Node, set[Edge]]
    """ Edges grouped by their from-nodes. """
    
    distances: dict[Node, float]
    """ Distance from every node to the final node. """
    
    
    def __init__(self, word_list: Iterable[str]):

        # Create graph nodes
        
        nodes: set[Node] = set()
        self.start_nodes = []
        final_node = Node('', 0)
        
        for word in word_list:
            caseless_word = word.casefold()
            length = len(caseless_word)
            
            for offset in range(-length, length):
                matching_part, tail = slice_by_offset(caseless_word, offset)
                from_node = Node(reverse(tail), offset)
                nodes.add(from_node)
                
                # A node is starting if its matching part is palindromic
                if matching_part == reverse(matching_part):
                    self.start_nodes.append((from_node, word))
        
        
        # Create edges
        
        edges_by_to_node: dict[Node, set[Edge]] = defaultdict(set)
        
        for from_node in nodes:
            for word in word_list:
                if edge := Edge.try_create(from_node, word):
                    edges_by_to_node[edge.to_node].add(edge)
        
        
        # Find distance from every node to the final node
        
        self.distances = defaultdict(lambda: inf)
        self.distances[final_node] = 0
        
        queue: PriorityQueue[Prioritized[Node]] = PriorityQueue()
        queue.put(Prioritized(0, final_node))
        
        while not queue.empty():
            prioritized = queue.get()
            from_node_distance = prioritized.priority + 1
            
            for edge in edges_by_to_node[prioritized.item]:
                from_node = edge.from_node
                if self.distances[from_node] > from_node_distance:
                    self.distances[from_node] = from_node_distance
                    queue.put(Prioritized(from_node_distance, from_node))
        
        
        # Group edges by from-node leaving only accessible ones
        
        self.edges_by_from_node = defaultdict(set)
        
        for edges in edges_by_to_node.values():
            for edge in edges:
                if self.distances[edge.from_node] < inf and self.distances[edge.to_node] < inf:
                    self.edges_by_from_node[edge.from_node].add(edge)


word = 'unpa'
length = len(word)
for offset in range(-length, length):
    matching_part, tail = slice_by_offset(word, offset)
    print(offset, matching_part, tail)
