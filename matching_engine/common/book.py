import logging
from typing import List

from sortedcontainers import SortedList

from matching_engine.common.message import OrderFullyFilled, OrderPartiallyFilled, TradeEvent
from matching_engine.common.message_publisher import MessagePublisher, MessagePublisherDefault
from matching_engine.common.order import Order
from matching_engine.common.side import SideEnum


class Book:

    def __init__(self, message_publisher: MessagePublisher = None) -> None:
        super().__init__()
        self._message_publisher = message_publisher or MessagePublisherDefault()

        self._buys = SortedList(key=lambda o: (-o.px, o.id))
        self._sells = SortedList(key=lambda o: (-o.px, -o.id))

        self._all_resting_orders_by_id = dict()

    def match(self, resting_orders, o: Order) -> List[Order]:
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

                self._message_publisher.publish(TradeEvent(q, ro.px))

                o.reduce(q)
                if o.qty > 0:
                    self._message_publisher.publish(OrderPartiallyFilled(o.id, o.qty))
                else:
                    self._message_publisher.publish(OrderFullyFilled(o.id))

                if q < ro.qty:
                    ro.reduce(q)
                    self._message_publisher.publish(OrderPartiallyFilled(ro.id, ro.qty))
                else:
                    filled_resting_orders.append(ro)
                    self._message_publisher.publish(OrderFullyFilled(ro.id))

        return filled_resting_orders

    def add(self, o: Order):
        add_to_book = self._sells if o.side == SideEnum.SELL else self._buys
        resting_orders = self._sells if o.side == SideEnum.BUY else self._buys

        for ro in self.match(resting_orders, o):
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
