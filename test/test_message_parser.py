import pytest
from matching_engine.common.message_parser import *
from matching_engine.common.message import *


class TestParserDefault:

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        self._parser = MessageParserDefault()
        yield

    def test_parse_add_order_request(self):
        r = self._parser.parse("0,100000,1,1,1075")
        assert isinstance(r, AddOrderRequest)
        assert isinstance(r.qty, int)
        assert r.qty == 1
        assert isinstance(r.px, float)
        assert r.px == 1075.0
        assert r.id == 100000
        assert r.msg_type == 0

        r = self._parser.parse(" 0,100000, 1,1,1075 ")
        assert isinstance(r, AddOrderRequest)
        assert isinstance(r.qty, int)
        assert r.qty == 1
        assert isinstance(r.px, float)
        assert r.px == 1075.0
        assert r.id == 100000
        assert r.msg_type == 0

    def test_parse_cancel_order_request(self):
        r = self._parser.parse("1,100004")
        assert isinstance(r, CancelOrderRequest)
        assert r.id == 100004
        assert r.msg_type == 1

        r = self._parser.parse(" 1 ,   100004 ")
        assert isinstance(r, CancelOrderRequest)
        assert r.id == 100004
        assert r.msg_type == 1

    def test_malformed_request(self):
        r = self._parser.parse("3,100004")
        assert r is None

        r = self._parser.parse("junk\n\n\n")
        assert r is None
