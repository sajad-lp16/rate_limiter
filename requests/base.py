from uuid import uuid4
from datetime import datetime
from dataclasses import (
    field,
    dataclass,
)


class Headers(dict):
    def __hash__(self) -> int:
        return hash(frozenset(self.items()))

    def __eq__(self, other: "Headers") -> bool:
        return hash(self) == hash(other)


@dataclass(order=True)
class Request:
    message: str = field(compare=False)
    uid: uuid4 = field(compare=False, default_factory=uuid4)
    priority: int = field(default=5)
    execution_time: datetime = field(compare=False, default=None)

    def __post_init__(self) -> None:
        if self.execution_time is not None:
            assert self.execution_time > datetime.now(), "execution time must be greater than now"

    def __str__(self) -> str:
        return f"Request(uid={self.uid}, message={self.message}, priority={self.priority}, execution_time={self.execution_time})"

    def __repr__(self) -> str:
        return self.__str__()
