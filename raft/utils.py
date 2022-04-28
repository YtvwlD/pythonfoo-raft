from typing import List, Optional, TypeVar

T = TypeVar("T")

def list_get(
    l: List[T], index: int, default: Optional[T] = None
) -> Optional[T]:
    """Get, but for lists."""
    if index < 0:
        return default
    try:
        return l[index]
    except IndexError:
        return default
