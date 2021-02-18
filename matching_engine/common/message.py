from typing import Set

from matching_engine.common.side import SideEnum

__all__ = ['MessageTypeEnum', 'Message', 'AddOrderRequest', 'CancelOrderRequest', 'TradeEvent', 'OrderPartiallyFilled',
           'OrderFullyFilled']


class MessageTypeEnum:
    _values = [
        0,
        1,
        2,
        3,
        4
    ]

    AddOrderRequest, CanceOrderRequest, TradeEvent, OrderFullyFilled, OrderPartiallyFilled = _values

    @classmethod
    def values(cls) -> Set[int]:
        return set(cls._values)


class Message:

    def __init__(self, msg_type: int) -> None:
        super().__init__()
        self._msg_type = int(msg_type)

    @property
    def msg_type(self) -> int:
        return self._msg_type

    def validate(self):
        assert self._msg_type in MessageTypeEnum.values(), f"Invalid msg type {self._msg_type}"


class AddOrderRequest(Message):
    """
    AddOrderRequest: msg_type,order_id,side,qty,px (e.g. 0,123,0,9,1000)
    msg_type   = 0
    id   = unique positive integer to identify each order;
              used to reference existing orders for remove/modify
    side  = 0 (Buy) or 1 (Sell)
    qty  = positive integer indicating maximum quantity to buy/sell
    px   = double indicating max price at which to buy/min price to sel
    """

    def __init__(self, id: int, side: int, qty: int, px: float) -> None:
        super().__init__(MessageTypeEnum.AddOrderRequest)
        self._id = int(id)
        self._side = int(side)
        self._qty = int(qty)
        self._px = float(px)

    def __str__(self) -> str:
        return f"{self._msg_type},{self._id},{self._side},{self._qty},{self._px}"

    @property
    def id(self) -> int:
        return self._id

    @property
    def side(self) -> int:
        return self._side

    @property
    def qty(self) -> int:
        return self._qty

    @property
    def px(self) -> float:
        return self._px


class CancelOrderRequest(Message):
    """
    CancelOrderRequest: msgtype,orderid (e.g. 1,123)
    msg_type   = 1
    id   = unique positive integer to identify each order;
              used to reference existing orders for remove/modify
    """

    def __init__(self, id: int) -> None:
        super().__init__(MessageTypeEnum.CanceOrderRequest)

        self._id = int(id)

    @property
    def id(self) -> int:
        return self._id

    def __str__(self) -> str:
        return f"{self._msg_type},{self._id}"


class TradeEvent(Message):
    """
    TradeEvent: msg_type,qty,px (e.g. 2,2,1025)
    msg_type   = 2
    qty  = amount that traded
    px     = price at which the trade happened
    """

    def __init__(self, qty: int, px: float) -> None:
        super().__init__(MessageTypeEnum.TradeEvent)
        self._qty = int(qty)
        self._px = float(px)

    @property
    def qty(self) -> int:
        return self._qty

    @property
    def px(self) -> float:
        return self._px

    def __str__(self) -> str:
        px = "{0:g}".format(self._px)
        return f"{self._msg_type},{self._qty},{px}"


class OrderFullyFilled(Message):
    """
    OrderFullyFilled: msg_type,order_id (e.g. 3,123)
    msg_type   = 3
    order_id   = ID of the order that was removed

    """

    def __init__(self, order_id: int) -> None:
        super().__init__(MessageTypeEnum.OrderFullyFilled)
        self._order_id = int(order_id)

    @property
    def order_id(self) -> int:
        return self._order_id

    def __str__(self) -> str:
        return f"{self._msg_type},{self.order_id}"


class OrderPartiallyFilled(Message):
    """
    OrderPartiallyFilled: msg_type,order_id,qty (e.g. 4,123,3)
    msg_type   = 4
    order_id   = ID of the order to modify
    qty  = The new quantity of the modified order.

    """

    def __init__(self, order_id: int, qty: int) -> None:
        super().__init__(MessageTypeEnum.OrderPartiallyFilled)
        self._order_id = order_id
        self._qty = qty

    @property
    def order_id(self) -> int:
        return self._order_id

    @property
    def qty(self) -> int:
        return self._qty

    def __str__(self) -> str:
        return f"{self._msg_type},{self.order_id},{self._qty}"
