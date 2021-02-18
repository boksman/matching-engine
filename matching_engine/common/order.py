class Order:
    def __init__(self, id: int, side: int, qty: int, px: float) -> None:
        super().__init__()
        self._id = id
        self._side = side
        self._qty = qty
        self._px = px

    @property
    def id(self) -> int:
        return self._id

    @property
    def side(self) -> int:
        return self._side

    @property
    def px(self) -> float:
        return self._px

    @property
    def qty(self) -> int:
        return self._qty

    def reduce(self, amount):
        self._qty -= amount

    def __str__(self) -> str:
        return f"{self.id} {self._side} {self._qty} {self.px}"