from __future__ import annotations
from typing import Iterable, Optional
from dataclasses import dataclass
from collections import defaultdict
from math import inf
from queue import PriorityQueue
from prioritized import Prioritized

# Helpar functions

def reverse(s: str) -> str:
    return s[::-1]

def slice_by_offset(word: str, offset: int) -> tuple[str, str]:
    if offset >= 0:
        return (word[offset:], word[:offset])
    else:
        return (word[:offset], word[offset:])

def sign(i: int) -> int:
    return 1 if i >= 0 else -1

# Classes

@dataclass(frozen=True)
class Node:
    """ Graph node representing a class of palindrome fragments with a common tail.
        `offset` is the signed length of the tail.
        If the tail is located before the pallindromic part, `offset` is >= 0.
        If the tail is located after the pallindromic part, `offset` is < 0.
    """
    tail: str
    offset: int
    
    def __post_init__(self):
        assert(len(self.tail) == abs(self.offset))
    
    def __repr__(self):
        return f'{self.tail}-' if self.offset >= 0 else f'-{self.tail}'


@dataclass(frozen=True)
class Edge:
    """ Edge between two graph nodes marked with a word.
        The edge exists iff `to_node` is reached by adding `word`
        to fragments from the `from_node` class.
    """
    from_node: Node
    word: str
    to_node: Node
    
    def __repr__(self):
        return f'{self.from_node} ({self.word})→ {self.to_node}'
    
    @classmethod
    def try_create(cls, from_node: Node, word: str) -> Optional[Edge]:
        """ Creates an edge by its `from_node` and `word`
            or returns None if impossible.
        """
        caseless_word = word.casefold()
        word_length = len(caseless_word)
        
        to_node_offset = from_node.offset - sign(from_node.offset) * word_length
        word_offset = -sign(to_node_offset) * word_length
        
        if sign(from_node.offset) == sign(to_node_offset):
            to_node_tail, tail_matching_part = slice_by_offset(from_node.tail, word_offset)
            word_matching_part = caseless_word
        else:
            to_node_tail, word_matching_part = slice_by_offset(caseless_word, from_node.offset)
            tail_matching_part = from_node.tail
        
        if reverse(tail_matching_part) == word_matching_part:
            return Edge(from_node, word, Node(to_node_tail, to_node_offset))
        else:
            return None


class PalindromeGraph:
    """ Helper graph for building palindromes.
        To build a palindrome, one should start with a start node
        and go along the edges till the final node.
        At each step, the word from the edge should be added to the fragment
        at the opposite side from the fragment's tail.
    """
    
    start_positions: list[tuple[Node, str]]
    """ Start nodes and corresponding start words. """
    
    edges_by_from_node: dict[Node, set[Edge]]
    """ Edges grouped by their from-nodes. """
    
    distances: dict[Node, float]
    """ Distance from every node to the final node. """
    
    
    def __init__(self, word_list: Iterable[str]):
        
        # Create graph nodes
        
        nodes: set[Node] = set()
        start_positions = []
        final_node = Node('', 0)
        
        for word in word_list:
            caseless_word = word.casefold()
            length = len(caseless_word)
            
            for offset in range(-length, length):
                matching_part, tail = slice_by_offset(caseless_word, offset)
                from_node = Node(tail, offset)
                nodes.add(from_node)
                
                # A node is starting if its matching part is palindromic
                if reverse(matching_part) == matching_part:
                    start_positions.append((from_node, word))
        
        
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
        
        
        # Leave only useful start positions
        
        self.start_positions = [(n, w) for n, w in start_positions if self.distances[n] < inf]
        
        
        # Group edges by from-node leaving only useful ones
        
        self.edges_by_from_node = defaultdict(set)
        
        for to_node, edges in edges_by_to_node.items():
            if self.distances[to_node] < inf:
                for edge in edges:
                    self.edges_by_from_node[edge.from_node].add(edge)
        
        
        # Nodes (Not used in generation. For debugging or visualizing purposes)
        
        self.nodes = [n for n in nodes if self.distances[n] < inf]
