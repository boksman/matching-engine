import abc
from typing import Optional

from .helpers import print_stderr, is_int
from .message import Message, MessageTypeEnum, AddOrderRequest, CancelOrderRequest

__all__ = ['MessageParser', 'MessageParserDefault']


class MessageParser(metaclass=abc.ABCMeta):
    def parse(self, line: str) -> Optional[Message]:
        """
        Interface for a message parser
        :param line: a string representing a message
        :return: Message or None
        """


class MessageParserDefault(MessageParser):
    request_type_cls_map = {
        MessageTypeEnum.AddOrderRequest: AddOrderRequest,
        MessageTypeEnum.CanceOrderRequest: CancelOrderRequest
    }

    def __init__(self) -> None:
        super().__init__()

    def parse(self, line: str) -> Optional[Message]:
        if line is None:
            return None
        line = line.strip()
        items = line.split(',')
        if len(items) < 2:
            return None

        msg_type = items[0]
        if not is_int(msg_type):
            print_stderr(f"Unhandled or malformed message '{line}'")
            return None

        cls = self.request_type_cls_map.get(int(msg_type), None)

        if cls is None:
            print_stderr(f"Unhandled or malformed message '{line}'")
            return None

        return cls(*items[1:])
