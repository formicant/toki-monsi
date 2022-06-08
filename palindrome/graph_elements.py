from dataclasses import dataclass


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
        assert (len(self.tail) == abs(self.offset))

    def __repr__(self):
        return f'{self.tail}-' if self.offset >= 0 else f'-{self.tail}'


@dataclass(frozen=True)
class StartEdge:
    """ Edge from the start to a graph node marked with a word.
        The edge exists iff `to_node` can be reached by starting with `word`.
    """
    word: str
    to_node: Node

    def __repr__(self):
        return f'({self.word})→ {self.to_node}'


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
