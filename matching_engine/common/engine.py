from matching_engine.common.book import Book
from matching_engine.common.message import Message, AddOrderRequest, CancelOrderRequest
from matching_engine.common.order import Order
import abc

__all__ = ['MatchingEngine', 'MatchingEngineDefault']


class MatchingEngine(metaclass=abc.ABCMeta):
    def process(self, message: Message):
        """
        Process a incoming messages
        :param message:
        :return:
        """


class MatchingEngineDefault(MatchingEngine):

    def __init__(self, book: Book = None) -> None:
        super().__init__()
        self._book = book or Book()

    def process(self, message: Message):
        if isinstance(message, AddOrderRequest):
            self._book.add(Order(message.id, message.side, message.qty, message.px))
        elif isinstance(message, CancelOrderRequest):
            self._book.remove(message.id)
        else:
            raise Exception(f"Unhandled request type '{message.msg_type}'")
