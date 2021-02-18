import pytest

from matching_engine.common.book import Book
from matching_engine.common.engine import *
from matching_engine.common.message import *
from matching_engine.common.message_publisher import MessagePublisherMock


class TestParserDefault:

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        self._msg_publisher = MessagePublisherMock()
        self._book = Book(message_publisher=self._msg_publisher)
        self._engine = MatchingEngineDefault(book=self._book)
        yield

    def test_scenario1(self):
        self._engine.process(AddOrderRequest(100000, 1, 1, 1075))
        assert len(self._msg_publisher.out) == 0
        self._engine.process(AddOrderRequest(100001, 0, 9, 1000))
        assert len(self._msg_publisher.out) == 0
        self._engine.process(AddOrderRequest(100002, 0, 30, 975))
        assert len(self._msg_publisher.out) == 0
        self._engine.process(AddOrderRequest(100003, 1, 10, 1050))
        assert len(self._msg_publisher.out) == 0
        self._engine.process(AddOrderRequest(100004, 0, 10, 950))
        assert len(self._msg_publisher.out) == 0
        self._engine.process(AddOrderRequest(100005, 1, 2, 1025))
        assert len(self._msg_publisher.out) == 0
        self._engine.process(AddOrderRequest(100006, 0, 1, 1000))
        assert len(self._msg_publisher.out) == 0
        self._engine.process(CancelOrderRequest(100004))
        assert len(self._msg_publisher.out) == 0
        self._engine.process(AddOrderRequest(100007, 1, 5, 1025))
        assert len(self._msg_publisher.out) == 0
        self._engine.process(AddOrderRequest(100008, 0, 3, 1050))
        assert len(self._msg_publisher.out) == 6

        results = '\n'.join([str(s) for s in self._msg_publisher.out])

        expected = "2,2,1025\n" \
                   "4,100008,1\n" \
                   "3,100005\n" \
                   "2,1,1025\n" \
                   "3,100008\n" \
                   "4,100007,4"

        assert results == expected
