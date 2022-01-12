from __future__ import annotations
from dataclasses import dataclass
from functools import total_ordering
from typing import TypeVar, Generic

T = TypeVar('T')

@total_ordering
@dataclass(frozen=True)
class Prioritized(Generic[T]):
    priority: int
    item: T
    
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Prioritized) and self.priority == other.priority
    
    def __lt__(self, other: Prioritized[T]) -> bool:
        return self.priority < other.priority
