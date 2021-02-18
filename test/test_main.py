import pytest

from matching_engine.app import main
from matching_engine.common.book import Book
from matching_engine.common.engine import *
from matching_engine.common.message_publisher import MessagePublisherMock


def test_main():
    test_in = """
       0,100000,1,1,1075
       0,100001,0,9,1000
       0,100002,0,30,975
       0,100003,1,10,1050
       0,100004,0,10,950
       BADMESSAGE
       0,100005,1,2,1025
       0,100006,0,1,1000
       1,100004
       0,100007,1,5,1025
       0,100008,0,3,1050
       """

    l = lambda: iter(test_in.strip().split('\n'))

    msg_publisher = MessagePublisherMock()
    book = Book(message_publisher=msg_publisher)

    main(input_iterator_func=l, engine=MatchingEngineDefault(book=book))

    results = '\n'.join([str(s) for s in msg_publisher.out])

    expected = "2,2,1025\n" \
               "4,100008,1\n" \
               "3,100005\n" \
               "2,1,1025\n" \
               "3,100008\n" \
               "4,100007,4"

    assert results == expected


if __name__ == "__main__":
    import os

    pytest.main([os.path.basename(__file__)])
