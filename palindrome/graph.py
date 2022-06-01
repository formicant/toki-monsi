from collections import defaultdict
from .graph_elements import Node, StartEdge, Edge
from .graph_building import get_start_edges, get_edges, calculate_distances

class PalindromeGraph:
    """ Helper graph for building palindromes.
        To build a palindrome, one should start with a start edge
        and go along the edges till the final node.
        At each step, the word from the edge should be added to the fragment
        at the opposite side from the fragment's tail.
    """
    
    start_edges: list[StartEdge]
    """ Edges to start from. """
    
    edges_from_node: dict[Node, list[Edge]]
    """ Edges grouped by their from-nodes. """
    
    distances: dict[Node, int]
    """ Distance from every node to the final node. """
    
    
    def __init__(self, word_list: list[str]):
        start_edges = list(get_start_edges(word_list))
        edges = list(get_edges(start_edges, word_list))
        
        self.distances = calculate_distances(edges)
        
        # Leave only useful start edges
        self.start_edges = [
            start_edge
            for start_edge in start_edges
            if start_edge.to_node in self.distances
        ]
        
        # Group edges by from-node leaving only useful ones
        self.edges_from_node = defaultdict(list)
        for edge in edges:
            if edge.to_node in self.distances:
                self.edges_from_node[edge.from_node].append(edge)
