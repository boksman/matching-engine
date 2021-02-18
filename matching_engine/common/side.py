from typing import Set


class SideEnum:
    _values = [
        0,
        1
    ]

    BUY, SELL = _values

    @classmethod
    def values(cls) -> Set[int]:
        return set(cls._values)