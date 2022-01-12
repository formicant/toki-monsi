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
        A tail is starting if it is located before the pallindromic part.
        Tails are stored with their characters in reversed order.
        If `reversed_tail` is empty, `is_starting` should be `True`!
    """
    reversed_tail: str
    is_starting: bool


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
        word_length = len(caseless_word)
        tail_length = len(from_node.reversed_tail)
        
        # TODO: simplify!
        if from_node.is_starting:
            if tail_length >= word_length:
                if not from_node.reversed_tail.startswith(caseless_word):
                    return None
                toNode = Node(from_node.reversed_tail[word_length:], True)
            else:
                if not caseless_word.startswith(from_node.reversed_tail):
                    return None
                toNode = Node(reverse(caseless_word[tail_length:]), False)
        else:
            if tail_length > word_length:
                if not from_node.reversed_tail.endswith(caseless_word):
                    return None
                toNode = Node(from_node.reversed_tail[:-word_length], False)
            else:
                if not caseless_word.endswith(from_node.reversed_tail):
                    return None
                toNode = Node(reverse(caseless_word[:-tail_length]), True)
        
        return Edge(from_node, word, toNode)


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
        final_node = Node('', True)
        
        for word in word_list:
            caseless_word = word.casefold()
            length = len(caseless_word)
            
            for offset in range(-length, length):
                matching_part, tail = slice_by_offset(caseless_word, offset)
                from_node = Node(reverse(tail), offset >= 0)
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
