from collections import defaultdict
from queue import PriorityQueue
from typing import Iterable, Optional

from .graph_elements import Node, StartEdge, Edge
from .prioritized import Prioritized


def get_start_edges(word_list: list[str]) -> Iterable[StartEdge]:
    for word in word_list:
        caseless_word = word.casefold()
        length = len(caseless_word)

        for offset in range(-length, length):
            to_node = try_create_start_node(caseless_word, offset)
            if to_node is not None:
                yield StartEdge(word, to_node)


def get_edges(
        start_edges: Iterable[StartEdge],
        word_list: list[str]
) -> Iterable[Edge]:

    visited_notes = {start_edge.to_node for start_edge in start_edges}
    stack = list(visited_notes)

    while len(stack) > 0:
        from_node = stack.pop()

        for word in word_list:
            caseless_word = word.casefold()

            to_node = try_create_next_node(from_node, caseless_word)
            if to_node is not None:
                yield Edge(from_node, word, to_node)
                if to_node not in visited_notes:
                    visited_notes.add(to_node)
                    stack.append(to_node)


def calculate_distances(edges: Iterable[Edge]) -> dict[Node, int]:
    """ Finds distance from every node to the final node.
    """
    from_nodes_by_to_node: dict[Node, list[Node]] = defaultdict(list)
    for edge in edges:
        from_nodes_by_to_node[edge.to_node].append(edge.from_node)

    final_node = Node('', 0)
    distances = {final_node: 0}

    queue: PriorityQueue[Prioritized[Node]] = PriorityQueue()
    queue.put(Prioritized(0, final_node))

    while not queue.empty():
        prioritized = queue.get()
        from_node_distance = prioritized.priority + 1

        for from_node in from_nodes_by_to_node[prioritized.item]:
            distance = distances.get(from_node)
            if distance is None or distance > from_node_distance:
                distances[from_node] = from_node_distance
                queue.put(Prioritized(from_node_distance, from_node))

    return distances


def try_create_start_node(caseless_word: str, offset: int) -> Optional[Node]:
    matching_part, tail = slice_by_offset(caseless_word, offset)

    # A node is accessible from start if the word's matching part is palindromic
    if reverse(matching_part) == matching_part:
        return Node(tail, offset)
    else:
        return None


def try_create_next_node(
        from_node: Node,
        caseless_word: str
) -> Optional[Node]:

    word_length = len(caseless_word)

    to_node_offset = from_node.offset - sign(from_node.offset) * word_length
    word_offset = -sign(to_node_offset) * word_length

    if sign(from_node.offset) == sign(to_node_offset):
        to_node_tail, tail_matching_part = slice_by_offset(from_node.tail,
                                                           word_offset)
        word_matching_part = caseless_word
    else:
        to_node_tail, word_matching_part = slice_by_offset(caseless_word,
                                                           from_node.offset)
        tail_matching_part = from_node.tail

    if reverse(tail_matching_part) == word_matching_part:
        return Node(to_node_tail, to_node_offset)
    else:
        return None


def slice_by_offset(word: str, offset: int) -> tuple[str, str]:
    if offset >= 0:
        return (word[offset:], word[:offset])
    else:
        return (word[:offset], word[offset:])


def reverse(s: str) -> str:
    return s[::-1]


def sign(i: int) -> int:
    return 1 if i >= 0 else -1
