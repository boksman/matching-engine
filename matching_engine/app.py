import logging
import os
from typing import Set, List, Union, Optional

from sortedcontainers import SortedList


class SideEnum:
    _values = [
        0,
        1
    ]

    BUY, SELL = _values

    @classmethod
    def values(cls) -> Set[int]:
        return set(cls._values)


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


def match(resting_orders, o: Order) -> List[Order]:
    """
    Given a collection of sorted resting orders match and reduce
    :param resting_orders:
    :param o:
    :return: filled orders that were at rest
    """

    filled_resting_orders = list()

    order_of_list = reversed(resting_orders) if o.side == SideEnum.BUY else resting_orders

    for ro in order_of_list:
        if o.qty <= 0:
            return filled_resting_orders

        if (o.px >= ro.px and o.side == SideEnum.BUY) or (o.px <= ro.px and o.side == SideEnum.SELL):
            q = min(o.qty, ro.qty)

            # todo: messages

            if q == ro.qty:
                filled_resting_orders.append(ro)
            else:
                ro.reduce(o.qty)

            o.reduce(q)

    return filled_resting_orders


class Book:

    def __init__(self) -> None:
        super().__init__()
        self._logger = logging.getLogger(self.__module__)
        self._buys = SortedList(key=lambda o: (-o.px, o.id))
        self._sells = SortedList(key=lambda o: (-o.px, -o.id))

        self._all_resting_orders_by_id = dict()

    def add(self, o: Order):
        add_to_book = self._sells if o.side == SideEnum.SELL else self._buys
        resting_orders = self._sells if o.side == SideEnum.BUY else self._buys

        for ro in match(resting_orders, o):
            resting_orders.remove(ro)
            del self._all_resting_orders_by_id[ro.id]

        if o.qty > 0:
            # add remaining to book
            add_to_book.add(o)
            self._all_resting_orders_by_id[o.id] = o

    def remove(self, id):
        o = self._all_resting_orders_by_id.pop(id)
        if o is not None:
            remove_from = self._sells if o.side == SideEnum.SELL else self._buys
            remove_from.remove(o)

    def print_book(self):

        print("\nThe Book")
        for i in self._sells:
            print(i)

        print("--------------")

        for i in self._buys:
            print(i)


class Message:

    def __init__(self, msg_type: int) -> None:
        super().__init__()
        self._msg_type = msg_type

    @property
    def msg_type(self) -> int:
        return self._msg_type

    def validate(self):
        assert self._msg_type in MessageTypeEnum.values(), f"Invalid msg type {self._msg_type}"


class AddOrderRequest(Message):
    """
    AddOrderRequest: msgtype,orderid,side,quantity,price (e.g. 0,123,0,9,1000)
    msg_type   = 0
    id   = unique positive integer to identify each order;
              used to reference existing orders for remove/modify
    side  = 0 (Buy) or 1 (Sell)
    qty  = positive integer indicating maximum quantity to buy/sell
    px   = double indicating max price at which to buy/min price to sel
    """

    def __init__(self, id: int, side: int, qty: int, px: float) -> None:
        super().__init__(MessageTypeEnum.AddOrderRequest)

        self._id = id
        self._side = side
        self._qty = qty
        self._px = px

    def validate(self):
        super().validate()
        assert self._side in SideEnum.values(), f"Invalid side {self._side}"
        assert isinstance(self._qty, int) and self._qty >= 0, f"Invalid qty {self._qty}"
        assert isinstance(self._px, float) and self._px >= 0, f"Invalid px {self._px}"
        assert isinstance(self._id, int) and self._id >= 0, f"Invalid id {self._id}"

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

        self._id = id

    def validate(self):
        super().validate()
        assert isinstance(self._id, int) and self._id >= 0, f"Invalid id {self._id}"

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
        self._qty = qty
        self._px = px

    @property
    def qty(self) -> int:
        return self._qty

    @property
    def px(self) -> float:
        return self._px

    def __str__(self) -> str:
        return f"{self._msg_type},{self._qty},{self._px}"


class OrderFullyFilled(Message):
    """
    OrderFullyFilled: msg_type,order_id (e.g. 3,123)
    msg_type   = 3
    order_id   = ID of the order that was removed

    """

    def __init__(self, order_id: int) -> None:
        super().__init__(MessageTypeEnum.OrderFullyFilled)
        self._order_id = order_id

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


request_type_cls_map = {
    MessageTypeEnum.AddOrderRequest: AddOrderRequest,
    MessageTypeEnum.CanceOrderRequest: CancelOrderRequest
}


def parse_request(line: str) -> Optional[Message]:
    if line is None:
        return None
    line = line.strip()
    items = line.split(',')
    if len(items) < 2:
        return None

    msg_type = items[0]
    cls = request_type_cls_map.get(msg_type, None)
    return cls(*items[1:])


def process_messages(book: Book, message: Message):
    if isinstance(message, AddOrderRequest):
        book.add(Order(message.id, message.side, message.qty, message.px))
    elif isinstance(message, CancelOrderRequest):
        book.remove(message.id)
    else:
        raise Exception(f"Unhandled request type '{message.msg_type}'")


def publish_message(message: Message):
    print(message)


def main():
    logger = logging.getLogger()
    env = os.getenv('ENV', 'dev')
    logger.info(f"Staring in {env}")

    book = Book()
    book.add(Order(100, SideEnum.BUY, 100, 1.0))
    book.add(Order(101, SideEnum.BUY, 100, 2.0))
    book.add(Order(102, SideEnum.BUY, 200, 2.0))

    book.add(Order(300, SideEnum.SELL, 100, 3.0))
    book.add(Order(400, SideEnum.SELL, 200, 3.0))
    book.add(Order(500, SideEnum.SELL, 300, 4.0))

    book.print_book()

    book.add(Order(600, SideEnum.BUY, 350, 4.0))
    book.add(Order(700, SideEnum.SELL, 350, 1.5))

    book.print_book()

    book.remove(700)
    book.print_book()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
