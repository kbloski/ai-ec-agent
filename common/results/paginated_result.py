from dataclasses import dataclass, field
from typing import Generic, List, TypeVar

T = TypeVar("T")


@dataclass
class PaginatedResult(Generic[T]):
    items: List[T]
    page: int
    page_size: int
    total_items: int
    total_pages: int = field(init=False)

    def __post_init__(self):
        if self.page_size <= 0:
            self.total_pages = 0
        else:
            self.total_pages = (
                self.total_items + self.page_size - 1
            ) // self.page_size