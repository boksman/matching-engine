import abc

__all__ = ['MessagePublisherDefault', 'MessagePublisher', 'MessagePublisherMock']


class MessagePublisher(metaclass=abc.ABCMeta):
    def publish(self, message):
        """
        Publish a message
        :param message:
        :return:
        """


class MessagePublisherDefault(MessagePublisher):
    """
    Just print to stdout
    """

    def publish(self, message):
        print(message)


class MessagePublisherMock(MessagePublisher):
    # Mock publisher
    def __init__(self) -> None:
        super().__init__()
        self.out = []

    def publish(self, message):
        self.out.append(message)
